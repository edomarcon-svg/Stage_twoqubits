"""Reports only consume saved data. Missing or invalid data are explicit."""
import csv
import html
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import qutip as qt
from .controls import Signal


def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path.with_suffix(".png"),dpi=150)
    fig.savefig(path.with_suffix(".pdf"))
    plt.close(fig)


def seed_figures(folder):
    folder = Path(folder)
    meta = json.loads((folder/"result.json").read_text())
    with np.load(folder/"arrays.npz",allow_pickle=False) as data:
        t = data["times"]
        fig,axs = plt.subplots(3,1,figsize=(9,8),sharex=True)
        for j,values in enumerate(data["physical_total_frequency"]):
            axs[0].plot(t,values,ls="-" if j==0 else "--",label=f"Qubit {j+1}")
        axs[0].set_ylabel("Frequenza totale [unità di riferimento]")
        axs[0].legend()
        axs[1].plot(t,data["mean_photons"],label="Numero medio fotoni")
        axs[1].set_ylabel("Numero medio fotoni")
        axs[1].legend()
        axs[2].plot(t,data["cavity_fidelity_root"],label="Fedeltà radice cavità")
        axs[2].plot(t,data["purity"],label="Purezza cavità")
        axs[2].set_xlabel("Tempo [unità inverse di frequenza]")
        axs[2].set_ylim(-.02,1.02)
        axs[2].legend()
        for ax in axs:
            ax.axvline(float(data["command_times"][-1]),color="gray",ls=":")
            ax.grid(alpha=.2)
        _save(fig,folder/"dynamics")
        target = data["target_cavity"]
        grid = data["wigner_grid"]
        wt = qt.wigner(qt.Qobj(target),grid,grid)
        wf = data["wigner_final"]
        limit = max(float(abs(wt).max()),float(abs(wf).max()),1e-12)
        norm = TwoSlopeNorm(vmin=-limit,vcenter=0,vmax=limit)
        fig,axs = plt.subplots(1,2,figsize=(10,4),layout="constrained")
        for ax,w,title in zip(axs,[wt,wf],["Target","Cavità finale (continua)"]):
            im = ax.pcolormesh(grid,grid,w,cmap="RdBu_r",norm=norm,shading="auto")
            ax.set(title=title,xlabel="x",ylabel="p",aspect="equal")
        fig.colorbar(im,ax=axs,label="W(x,p)")
        fig.savefig(folder/"wigner.png",dpi=150)
        fig.savefig(folder/"wigner.pdf")
        plt.close(fig)
        fig,axs = plt.subplots(1,2,figsize=(10,4))
        axs[0].plot(data["crab_history"],label="CRAB")
        if "grape_history" in data:
            axs[0].plot(data["grape_history"],label="GRAPE")
        axs[0].set(xlabel="Valutazione obiettivo",ylabel="Costo configurato (vedi config.json)")
        axs[0].legend()
        ns = np.arange(len(target))
        axs[1].bar(ns,abs(target)**2,alpha=.5,label="Target")
        axs[1].plot(ns,data["photon_distribution"],"o",ms=3,label="Finale")
        axs[1].set(xlabel="Numero fotoni",ylabel="Probabilità")
        axs[1].legend()
        _save(fig,folder/"optimization")
        cfg = json.loads((folder.parents[1]/"config.json").read_text())
        signal = Signal(float(data["command_times"][-1]),len(data["command_times"]),cfg["control"]["filter_cutoff"])
        dense_t = np.linspace(0,signal.duration,4001)
        delivered = signal.values(data["physical_command_modulation"],dense_t)
        fig,axs = plt.subplots(1,2,figsize=(11,4))
        for j,delta in enumerate(delivered):
            line, = axs[0].plot(dense_t,delta,label=f"Applicato Q{j+1}",ls="-" if j==0 else "--")
            axs[0].plot(data["command_times"],data["physical_command_modulation"][j],ls=":",alpha=.55,color=line.get_color(),label=f"Comando Q{j+1}")
            ac=delta[:-1]-np.mean(delta[:-1])
            omega=2*np.pi*np.fft.rfftfreq(len(ac),dense_t[1]-dense_t[0])
            power=abs(np.fft.rfft(ac))**2
            if power.max()>0:
                power/=power.max()
            axs[1].plot(omega,power,label=f"Q{j+1}",ls="-" if j==0 else "--")
        cutoff=cfg["control"]["filter_cutoff"]
        if cutoff is not None:
            axs[1].axvline(cutoff,ls=":",color="gray",label="Polo del filtro")
        max99=meta["actuator"]["omega_99_worst_channel"]
        axs[1].set_xlim(0,max(6.,2*max99,2*(cutoff or 0)))
        axs[0].set(xlabel="Tempo",ylabel="Modulazione della frequenza")
        axs[1].set(xlabel="Frequenza angolare",ylabel="Potenza FFT relativa (AC)")
        for ax in axs:
            ax.legend(fontsize=8)
            ax.grid(alpha=.2)
        _save(fig,folder/"actuator")
        if "photon_populations" in data:
            fig,axs = plt.subplots(2,1,figsize=(10,7),sharex=True)
            im = axs[0].pcolormesh(t,np.arange(data["photon_populations"].shape[1]),
                data["photon_populations"].T,shading="auto",cmap="viridis")
            fig.colorbar(im,ax=axs[0],label="Popolazione")
            axs[0].set_ylabel("Numero fotoni")
            axs[1].plot(t,data["target_probability_trajectory"],label="P target (include eventuale reset)")
            axs[1].axvline(signal.duration,ls=":",color="gray")
            axs[1].set(xlabel="Tempo",ylabel="Probabilità",ylim=(-.02,1.02))
            axs[1].legend()
            _save(fig,folder/"populations")
    return meta


def write_reports(root, make_figures=True):
    root = Path(root)
    summary = json.loads((root/"summary.json").read_text())
    config = json.loads((root/"config.json").read_text())
    timing = f"Durata fisica T = {config['duration']:.10g}."
    if config.get("factor_taus") is not None:
        tau_s = np.pi/(2*config["tau_s_coupling"])
        timing += f" T = {config['factor_taus']} × tau_s; tau_s = pi/(2*g_ref) = {tau_s:.10g}, g_ref = {config['tau_s_coupling']:.10g}."
    rows = []
    for case in summary["cases"]:
        for item in case["seeds"] + case.get("warm_starts",[]):
            folder = root/item["folder"]
            if make_figures:
                seed_figures(folder)
            rows.append({"case":case["name"],"seed":item["seed"],"cohort":item.get("cohort","random"),"P_target":item["metrics"]["target_probability"],
                "F_root":item["metrics"]["fidelity_root"],"purezza":item["metrics"]["purity"],
                "validato":item["validation"]["passed"],"obiettivo_raggiunto":item["metrics"]["goal_reached"],
                "fluence_modulazione":item["actuator"]["modulation_fluence_total"],
                "banda99_peggiore":item["actuator"]["omega_99_worst_channel"],
                "potenza_sopra_soglia":item["actuator"].get("ac_power_fraction_above_threshold_worst"),
                "P_iniziale":item["crab"].get("initial_probability"),
                "P_CRAB":item["crab"]["target_probability"],
                "guadagno_GRAPE":item["grape"].get("probability_gain"),
                "iterazioni_GRAPE":item["grape"]["iterations"],
                "gradiente_proiettato_iniziale":item["grape"].get("initial_gradient",{}).get("projected_gradient_max"),
                "gradiente_proiettato_finale":item["grape"].get("final_gradient",{}).get("projected_gradient_max"),
                "max_fotoni":item["metrics"].get("max_mean_photons_preparation"),
                "P_hold_min":(item.get("hold_summary") or {}).get("minimum_target_probability"),
                "cartella":item["folder"]})
    columns = list(rows[0]) if rows else ["case","seed"]
    with (root/"summary.csv").open("w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f,fieldnames=columns)
        w.writeheader()
        w.writerows(rows)
    text = ["# Risultati v2", "", timing, "", "Ogni riga usa la propagazione continua del controllo con il filtro configurato.",
        "P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.",
        "Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.",
        "Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.",
        "La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.","",
        "| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |", "|---|---:|---:|---:|---:|---|---|"]
    for row in rows:
        text.append(f"| {row['case']} | {row['seed']} | {row['P_target']:.8f} | {row['F_root']:.8f} | {row['purezza']:.6f} | {row['validato']} | {row['obiettivo_raggiunto']} |")
    for case in summary["cases"]:
        text += ["",f"## {case['name']}",f"Distribuzione sulle {len(case['seeds'])} pipeline raffinate: {json.dumps(case['statistics'],ensure_ascii=False)}.",
                 f"Seed selezionato: {case['selected_seed']}. Selezione per costo continuo, dando precedenza alle soluzioni validate."]
        if "baseline" in case:
            text.append(f"Probabilità target senza modulazione: {case['baseline']['metrics']['target_probability']:.8f}.")
        for item in case["seeds"] + case.get("warm_starts",[]):
            failed = [k for k,ok in item["validation"]["checks"].items() if not ok]
            text += ["",f"### {item.get('cohort','random')} — {item['seed']}",f"Controlli numerici falliti: {', '.join(failed) or 'nessuno'}.",
                     f"CRAB: {item['crab']['message']}. GRAPE: {item['grape']['message']}.",
                     f"[Metadati completi]({item['folder']}/result.json)"]
            for figure in ["dynamics","wigner","actuator","populations"]:
                if (root/item["folder"]/(figure+".png")).exists():
                    text.append(f"![{figure}]({item['folder']}/{figure}.png)")
    (root/"report.md").write_text("\n".join(text)+"\n",encoding="utf-8")
    body = ["<h1>Risultati v2</h1><p>Propagazione continua indipendente. P = probabilità target; F = √P.</p>",
            f"<p>{html.escape(timing)}</p>",
            "<p>Validazione numerica, raggiungimento del target e convergenza dell'ottimizzatore sono criteri distinti. Nessun risultato implica da solo un quantum speed limit.</p>",
            "<p><a href='summary.csv'>Tabella CSV</a> · <a href='config.json'>Configurazione</a> · <a href='provenance.json'>Provenienza</a></p>",
            "<table><tr>"+"".join(f"<th>{html.escape(c)}</th>" for c in columns if c!="cartella")+"</tr>"]
    for row in rows:
        body.append("<tr>"+"".join(f"<td>{html.escape(f'{value:.6g}' if isinstance(value,float) else str(value))}</td>" for key,value in row.items() if key!="cartella")+"</tr>")
    body.append("</table>")
    for case in summary["cases"]:
        body.append(f"<h2>{html.escape(case['name'])}</h2><p>Statistiche: {html.escape(json.dumps(case['statistics'],ensure_ascii=False))}</p>")
        if "baseline" in case:
            body.append(f"<p>Probabilità target senza modulazione: {case['baseline']['metrics']['target_probability']:.8f}.</p>")
        for item in case["seeds"] + case.get("warm_starts",[]):
            path = html.escape(item["folder"],quote=True)
            failures = [k for k,ok in item["validation"]["checks"].items() if not ok]
            body.append(f"<h3>Seed {item['seed']}</h3><p>Controlli falliti: {html.escape(', '.join(failures) or 'nessuno')}</p><a href='{path}/result.json'>Dettagli</a>")
            body.append(f"<p>{html.escape(item['crab']['message'])}; {html.escape(item['grape']['message'])}</p>")
            for figure in ["dynamics","wigner","optimization","actuator","populations"]:
                if (root/item["folder"]/(figure+".png")).exists():
                    body.append(f"<a href='{path}/{figure}.pdf'><img src='{path}/{figure}.png' alt='{figure}'></a>")
    document = "<!doctype html><html lang='it'><meta charset='utf-8'><title>Simulazioni v2</title><style>body{font:16px system-ui;max-width:1200px;margin:30px auto;padding:20px;color:#172033}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:8px;border:1px solid #ccc}th{background:#eef3fa}img{max-width:100%;height:auto}a{color:#165aa7}</style><body>"+"\n".join(body)+"</body></html>"
    (root/"report.html").write_text(document,encoding="utf-8")
