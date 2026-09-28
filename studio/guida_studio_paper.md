# Guida Interattiva allo Studio del Paper
## *"Engineering Nonclassical States via the Dynamical Casimir Effect"*
**Autori:** Maristella Crotti, Luca Razzoli, Giacomo Guarnieri, Luigi Giannelli, Giuseppe A. Falci, Giuliano Benenti  
*(Data di pubblicazione: Luglio 2026)*

---

> [!TIP]
> **Come usare questo documento interattivo di studio:**
> 1. **Testo del Paper**: Nella [Parte 1](#parte-1--traduzione-integrale-e-annotata-del-paper) trovi la traduzione fedele e accurata del testo dell'articolo, diviso per sezioni.
> 2. **Box di Approfondimento Fisico**: Ogni volta che incontri un concetto fisico non banale (USC, termini contro-rotanti, DCE, parità, CRAB, GRAPE, GKLS, Wigner), troverai un link `🔍 [Approfondimento Fisico #N]`. Cliccandoci verrai rimandato alla relativa scheda didattica nella [Parte 2](#parte-2--schede-didattiche-di-approfondimento-fisico).
> 3. **Interazione Continua**: Se durante la lettura una formula, un passaggio matematico o un concetto non ti è chiaro o vuoi vedere una dimostrazione passo per passo, **chiedimelo in chat**! Io aggiornerò direttamente questo file aggiungendo la risposta nel [Registro Approfondimenti su Richiesta (Q&A)](#parte-3--registro-approfondimenti-su-richiesta-qa).

---

## Indice Generale

* [Parte 1 — Traduzione Integrale e Annotata del Paper](#parte-1--traduzione-integrale-e-annotata-del-paper)
  * [Abstract](#abstract)
  * [1. Introduzione](#1-introduzione)
  * [2. Il Modello Fisico](#2-il-modello-fisico)
  * [3. Strategia di Controllo Ottimo Quantistico](#3-strategia-di-controllo-ottimo-quantistico)
  * [4. Generazione di Stati di Fock e Scaling con il Numero di Fotoni](#4-generazione-di-stati-di-fock-e-scaling-con-il-numero-di-fotoni)
  * [5. Robustezza al Rumore Classico e Quantistico](#5-robustezza-al-rumore-classico-e-quantistico)
  * [6. Conclusioni e Discussione](#6-conclusioni-e-discussione)
  * [Appendice A: Generazione di Stati Squeezed](#appendice-a-generazione-di-stati-squeezed)
  * [Appendice B: Generazione di Superposizioni di Stati Gatto di Schrödinger](#appendice-b-generazione-di-superposizioni-di-stati-gatto-di-schrödinger)
* [Parte 2 — Schede Didattiche di Approfondimento Fisico](#parte-2--schede-didattiche-di-approfondimento-fisico)
  * [Scheda 1: Dal Modello di Jaynes-Cummings al Modello di Rabi e al Regime Ultrastro (USC)](#scheda-1-dal-modello-di-jaynes-cummings-al-modello-di-rabi-e-al-regime-ultrastro-usc)
  * [Scheda 2: Termini Contro-Rotanti ed Effetto Casimir Dinamico (DCE) Parametrico](#scheda-2-termini-contro-rotanti-ed-effetto-casimir-dinamico-dce-parametrico)
  * [Scheda 3: La Conservazione della Parità e le Regole di Selezione](#scheda-3-la-conservazione-della-parità-e-le-regole-di-selezione)
  * [Scheda 4: Metodi di Controllo Ottimo: CRAB vs GRAPE vs Interpolazione PCHIP](#scheda-4-metodi-di-controllo-ottimo-crab-vs-grape-vs-interpolazione-pchip)
  * [Scheda 5: Funzionale di Costo Energetico $C^2$ e Vincoli di Fattibilità Sperimentale](#scheda-5-funzionale-di-costo-energetico-c2-e-vincoli-di-fattibilità-sperimentale)
  * [Scheda 6: La Funzione di Wigner e la Negatività nello Spazio delle Fasi](#scheda-6-la-funzione-di-wigner-e-la-negatività-nello-spazio-delle-fasi)
  * [Scheda 7: Rumore di Controllo ed Equazione Master di Lindblad (GKLS) con Bagno Ohmico](#scheda-7-rumore-di-controllo-ed-equazione-master-di-lindblad-gkls-con-bagno-ohmico)
  * [Scheda 8: Stati Squeezed e Misura in Decibel (dB)](#scheda-8-stati-squeezed-e-misura-in-decibel-db)
  * [Scheda 9: Stati Gatto di Schrödinger e Sovrapposizioni su Assi Ortogonali](#scheda-9-stati-gatto-di-schrödinger-e-sovrapposizioni-su-assi-ortogonali)
* [Parte 3 — Registro Approfondimenti su Richiesta (Q&A)](#parte-3--registro-approfondimenti-su-richiesta-qa)
  * [Q&A #1: Origine Fisica delle Proporzionalità di Tensione e Carica/Dipolo](#qa-1--origine-fisica-delle-proporzionalità-di-tensione-e-caricadipolo)
  * [Q&A #2: Gli Stati Non-Classici dell'Oscillatore Armonico nel Paper](#qa-2--gli-stati-non-classici-delloscillatore-armonico-nel-paper)
  * [Q&A #3: Gli Autostati $u_n(x)$ non sono gli "stati classici"? Il Paradosso degli Stati di Fock](#qa-3--gli-autostati-unx-non-sono-gli-stati-classici-il-paradosso-degli-stati-di-fock)
  * [Q&A #4: Creare uno Stato di Fock eccitando i Qubit: cosa stiamo facendo davvero?](#qa-4--creare-uno-stato-di-fock-eccitando-i-qubit-cosa-stiamo-facendo-davvero)
  * [Q&A #5: L'Effetto Casimir Dinamico (DCE): è programmato nel codice o emerge dalla fisica?](#qa-5--leffetto-casimir-dinamico-dce-è-programmato-nel-codice-o-emerge-dalla-fisica)
  * [Q&A #6: Cosa Significa che "È Conservata la Parità"? Regole di Selezione e Creazione a Coppie](#qa-6--cosa-significa-che-è-conservata-la-parità-regole-di-selezione-e-creazione-a-coppie)

---

# Parte 1 — Traduzione Integrale e Annotata del Paper

### Abstract
Il pilotaggio non-adiabatico (*nonadiabatic driving*) in sistemi luce-materia fortemente accoppiati è comunemente considerato una sorgente di errore, poiché le interazioni contro-rotanti convertono le fluttuazioni del vuoto in eccitazioni reali attraverso l'effetto Casimir dinamico (DCE) 🔍 [Scheda 2](#scheda-2-termini-contro-rotanti-ed-effetto-casimir-dinamico-dce-parametrico). In questo lavoro mostriamo che, al contrario, il DCE può essere sfruttato come risorsa per ingegnerizzare stati non-classici della luce. Considerando un modo di cavità accoppiato in modo ultrastro (*ultrastrongly coupled*) a un qubit a frequenza sintonizzabile 🔍 [Scheda 1](#scheda-1-dal-modello-di-jaynes-cummings-al-modello-di-rabi-e-al-regime-ultrastro-usc), impieghiamo il controllo ottimo quantistico 🔍 [Scheda 4](#scheda-4-metodi-di-controllo-ottimo-crab-vs-grape-vs-interpolazione-pchip) per progettare protocolli di pilotaggio che trasformano le fluttuazioni del vuoto in stati desiderati. L'ottimizzazione numerica rivela un approccio versatile e robusto per la preparazione deterministica di un'ampia classe di stati non-classici, qui illustrata tramite stati di Fock, stati *squeezed* e sovrapposizioni di stati gatto di Schrödinger (*Schrödinger-cat-state superpositions*).

---

### 1. Introduzione
La generazione di stati non-classici della luce è un obiettivo chiave nelle tecnologie quantistiche, con applicazioni nell'elaborazione dell'informazione quantistica e nella metrologia quantistica ad alta precisione [1, 2]. Gli stati *squeezed* consentono misurazioni oltre il limite quantistico standard [3, 4], come esemplificato dai rivelatori di onde gravitazionali (LIGO/Virgo) [5], mentre gli stati di Fock costituiscono una risorsa fondamentale per il calcolo quantistico bosonico [6]. Studi recenti hanno mostrato che modi bosonici inizializzati in stati di Fock possono persino fornire l'energia necessaria per implementare porte quantistiche arbitrarie mediante meccanismi di riciclo dell'energia [7]. Più in generale, sovrapposizioni di stati di Fock e stati gatto di Schrödinger costituiscono la base di diversi schemi di correzione d'errore quantistico bosonico e di codifica logica [8–11].

La capacità di preparare rapidamente stati non-classici prima che la decoerenza degradi le loro proprietà quantistiche è un requisito essenziale. L'elettrodinamica quantistica in circuiti (*Circuit QED*) offre una piattaforma promettente a tale scopo, consentendo l'accesso al regime di accoppiamento luce-materia ultrastro (*Ultrastrong Coupling*, USC) [12–14] 🔍 [Scheda 1](#scheda-1-dal-modello-di-jaynes-cummings-al-modello-di-rabi-e-al-regime-ultrastro-usc), in cui la forza dell'interazione diventa confrontabile con le frequenze naturali dei sottosistemi non accoppiati. La rapida dinamica luce-materia che ne risulta apre nuove opportunità per l'ingegnerizzazione efficiente di stati non-classici.

Tuttavia, spingere i protocolli di generazione di stati nel regime USC porta inevitabilmente in gioco l'effetto Casimir dinamico (DCE) [15–20], poiché la modulazione non-adiabatica dei parametri del sistema genera coppie di eccitazioni dal vuoto 🔍 [Scheda 2](#scheda-2-termini-contro-rotanti-ed-effetto-casimir-dinamico-dce-parametrico). Fino a oggi, il DCE è stato prevalentemente considerato come un effetto indesiderato che limita la fedeltà delle operazioni quantistiche [21]. Una notevole eccezione è la proposta pionieristica di sfruttarlo come risorsa per generare stati entangled di qubit superconduttori [22].

In questo lavoro, sfruttiamo il DCE come risorsa per la generazione rapida e deterministica di stati non-classici di cavità. A tale scopo, consideriamo una cavità elettromagnetica a singolo modo accoppiata a un sistema a due livelli (qubit) nel regime USC. In questo regime, i termini contro-rotanti giocano un ruolo cruciale, permettendo la generazione di fotoni dal vuoto tramite la modulazione non-adiabatica della frequenza del qubit, manifestazione del DCE parametrico [16]. Impiegando tecniche di controllo ottimo [23–26], progettiamo protocolli di pilotaggio che guidano il sistema verso gli stati non-classici desiderati massimizzando la fedeltà dello stato finale.

Illustriamo la versatilità dell'approccio mediante la generazione di stati bersaglio rappresentativi, inclusi stati di Fock, stati *squeezed* e sovrapposizioni di stati gatto di Schrödinger. Valutiamo sistematicamente le prestazioni in termini di fedeltà e costo di controllo su un ampio intervallo di parametri. Inoltre, dimostriamo la robustezza sia contro il rumore di controllo classico sia contro la dissipazione quantistica indotta da un ambiente termico. I nostri risultati stabiliscono un quadro operativo praticabile per utilizzare il DCE come risorsa per la generazione rapida e robusta di stati di cavità non-classici ad alta fedeltà.

---

### 2. Il Modello Fisico
Consideriamo una cavità elettromagnetica a singolo modo ad alto fattore di merito accoppiata a un sistema a due livelli (qubit) [12, 27], pilotata da un campo di controllo dipendente dal tempo che agisce sulla frequenza del qubit (si veda la Fig. 1). Il sistema è descritto dall'Hamiltoniana:
$$H_S(t) = H_R + H_D(t)$$

dove l'interazione cavità-qubit è descritta dall'**Hamiltoniana di Rabi** [28–30] (ponendo $\hbar = 1$):
$$H_R = \frac{\omega_q}{2} \sigma_z + \omega_c a^\dagger a + g (a^\dagger + a)(\sigma_+ + \sigma_-) \quad \text{(Eq. 1)}$$

e l'Hamiltoniana di controllo è data da:
$$H_D(t) = \frac{\Omega_D(t)}{2} \sigma_z \quad \text{(Eq. 2)}$$

Qui, $a$ ($a^\dagger$) è l'operatore bosonico di distruzione (creazione), $\sigma_+ = |e\rangle\langle g|$ ($\sigma_- = \sigma_+^\dagger$) è l'operatore di innalzamento (abbassamento) del qubit, $\sigma_z = |e\rangle\langle e| - |g\rangle\langle g|$ è l'operatore di Pauli-$z$, $\omega_c$ ($\omega_q$) è la frequenza della cavità (qubit), $g$ indica la costante di accoppiamento luce-materia, e $\Omega_D(t)$ è il campo classico esterno di pilotaggio (*drive*). Lo stato $|g\rangle$ ($|e\rangle$) è lo stato fondamentale (eccitato) del qubit.

Ci concentriamo sul **regime USC** ($g/\omega_c \gtrsim 0.1$) [12–14], in cui i termini contro-rotanti nell'interazione cavità-qubit, $a\sigma_- + a^\dagger\sigma_+$, non sono più trascurabili e contribuiscono in modo significativo alla dinamica del sistema 🔍 [Scheda 1](#scheda-1-dal-modello-di-jaynes-cummings-al-modello-di-rabi-e-al-regime-ultrastro-usc). Questi termini **rompono la conservazione del numero totale di eccitazioni**,
$$n_{\text{ex}} = a^\dagger a + \sigma_+ \sigma_-$$
permettendo ai fotoni di essere generati dal vuoto tramite il DCE [15–19, 31, 32].

Sebbene il numero di eccitazioni non sia conservato, la **parità**:
$$\Pi = e^{i\pi n_{\text{ex}}}$$
è conservata sia dall'Hamiltoniana di Rabi [30, 33] sia da quella di controllo; pertanto, **le eccitazioni vengono create o annichilite a coppie** 🔍 [Scheda 3](#scheda-3-la-conservazione-della-parità-e-le-regole-di-selezione).

---

### 3. Strategia di Controllo Ottimo Quantistico
Modulando la frequenza istantanea del qubit $\omega_q + \Omega_D(t)$, sfruttiamo il DCE per indurre eccitazioni nella cavità in modo controllato. Nello specifico, inizializziamo il sistema nello stato fondamentale congiunto:
$$|\psi_0\rangle = |0\rangle |g\rangle$$
dove $|0\rangle$ indica il vuoto della cavità.

In assenza di termini contro-rotanti (modello di Jaynes-Cummings standard), questo stato rimarrebbe identicamente invariato sotto qualsiasi modulazione della frequenza del qubit. Al contrario, in presenza di termini contro-rotanti, la modulazione può allontanare il sistema dal vuoto e guidarlo verso stati bersaglio non-classici della cavità, come gli stati di Fock, stati *squeezed* e sovrapposizioni di stati cat.

A questo scopo, impieghiamo il formalismo del controllo ottimo quantistico [23] per sagomare la modulazione temporale $\Omega_D(t)$ del drive (Eq. 2). Assumendo che il sistema si evolva dal tempo $t = 0$ al tempo finale $t = T$, l'obiettivo di controllo è massimizzare la fedeltà $F$ tra lo stato finale evoluto e lo stato bersaglio di cavità scelto. Ciò si ottiene ottimizzando il polso di controllo per minimizzare la funzione di costo definita dall'**infedeltà**:
$$C = 1 - F$$

Adottiamo una **strategia ibrida di controllo ottimo** che combina metodi *gradient-free* e *gradient-based* 🔍 [Scheda 4](#scheda-4-metodi-di-controllo-ottimo-crab-vs-grape-vs-interpolazione-pchip):
1. **CRAB (Chopped Random Basis)**: metodo *gradient-free* in cui il campo di controllo è parametrizzato come una serie di Fourier troncata:
   $$\Omega_D(t) = s(t) \sum_{k=1}^{N_f} [A_k \sin(\omega_k t) + B_k \cos(\omega_k t)] \quad \text{(Eq. 3)}$$
   dove $\{A_k, B_k\}$ sono parametri variazionali da ottimizzare, $N_f$ è il numero di armoniche, e le $\omega_k$ sono frequenze campionate casualmente. Questa parametrizzazione produce intrinsecamente campi di controllo lisci, mentre la funzione inviluppo $s(t)$ garantisce l'accensione e lo spegnimento graduale del drive esterno, imponendo $\Omega_D(0) = \Omega_D(T) = 0$. Fissare la norma dei coefficienti di Fourier vincola la potenza di controllo totale, restringendo l'ottimizzazione CRAB a regimi fisicamente realistici.
2. **GRAPE (Gradient Ascent Pulse Engineering)**: la soluzione fornita da CRAB viene usata come stima iniziale (*initial guess*) di alta qualità per GRAPE [26], un metodo basato su gradiente. Ciò permette a GRAPE di raffinare il profilo del polso per aumentare la fedeltà finale. In GRAPE, l'intervallo temporale totale $[0, T]$ è discretizzato in $N_t$ intervalli di durata $\delta t = T / N_t$, e il campo di controllo è rappresentato come una funzione costante a tratti:
   $$\Omega_D(t) \to \{\Omega_D^{(1)}, \Omega_D^{(2)}, \dots, \Omega_D^{(N_t)}\}$$
   Le ampiezze di controllo $\{\Omega_D^{(k)}\}$ vengono aggiornate iterativamente tramite gradienti analitici della funzione di costo, imponendo vincoli di ampiezza (*box constraints*) per rispettare le limitazioni di potenza sperimentali.
3. **Interpolazione Finale**: un passaggio conclusivo di interpolazione (spline/PCHIP) liscia il campo di controllo a tratti, producendo un polso continuo e sperimentalmente realizzabile con una perdita trascurabile di fedeltà.

Infine, ispirandoci ai metodi di pilotaggio contro-diabatico (*counterdiabatic driving*) [35, 36], per quantificare il costo energetico dei campi di controllo calcoliamo il seguente funzionale di costo indipendente dallo stato e dal setup:
$$C^2(t) := \int_0^t ds \, \|H_D(s)\|_2^2 \quad \text{(Eq. 4)}$$
dove $\|X\|_2 = \sqrt{\text{Tr}[X^\dagger X]}$ indica la norma di Frobenius 🔍 [Scheda 5](#scheda-5-funzionale-di-costo-energetico-c2-e-vincoli-di-fattibilità-sperimentale).

---

### 4. Generazione di Stati di Fock e Scaling con il Numero di Fotoni
Per dimostrare l'efficacia del protocollo, affrontiamo come primo banco di prova la generazione di uno stato di Fock altamente non-classico con $n = 6$ (si veda la Fig. 2). Partendo dal vuoto, il drive di controllo ottimizzato [pannello (a)] guida la popolazione della cavità [pannello (b)] preparando con successo lo stato desiderato $|n = 6\rangle$ con una **fedeltà di $F \approx 0.995$** su un tempo totale di evoluzione $T = 20\,\tau_s$, dove:
$$\tau_s = \frac{\pi}{2g}$$
fissa la scala temporale caratteristica (pari al tempo di mezza oscillazione di Rabi nel vuoto nel limite risonante di Jaynes-Cummings). L'eccellente accuratezza del protocollo è ulteriormente confermata dalla **funzione di Wigner** dello stato finale, che riproduce fedelmente gli anelli di interferenza concentrici alternati caratteristici dello stato target ideale [pannelli (c) e (d)] 🔍 [Scheda 6](#scheda-6-la-funzione-di-wigner-e-la-negatività-nello-spazio-delle-fasi).

Per valutare lo scaling delle prestazioni all'aumentare del numero di fotoni, indaghiamo la generazione di stati di Fock nell'intervallo $1 \le n \le 10$. Consideriamo innanzitutto l'ottimizzazione CRAB pura, senza raffinamento GRAPE o vincoli sulle ampiezze:
* Per ciascun $n$, la fedeltà e il costo vengono mediati su 10 ottimizzazioni CRAB indipendenti con semi casuali differenti (Fig. 3).
* La fedeltà media è costantemente elevata, **$F \gtrsim 0.96$ su tutti gli stati target** [pannello (a)], confermando la robustezza della strategia oltre il regime di bassa eccitazione.
* All'aumentare di $n$, la fedeltà media diminuisce gradualmente e la sua dispersione statistica si allarga, indicando un *landscape* di ottimizzazione via via più complesso.
* Coerentemente, il costo $C^2$ [pannello (b)] cresce moderatamente con $n$, riflettendo le maggiori risorse energetiche necessarie per creare stati di Fock fortemente eccitati.

La Figura 3 presenta inoltre i risultati ottenuti prendendo, per ogni $n$, la migliore soluzione CRAB come punto di partenza per il raffinamento GRAPE vincolato, seguito dallo smoothing. La fedeltà raffinata supera sistematicamente la media del CRAB puro (raggiungendo $F > 0.99$), in particolare nel regime di grande $n$. **Cosa fondamentale, il costo di controllo si riduce drasticamente**, dimostrando che i vincoli di ampiezza guidano efficacemente l'algoritmo verso soluzioni molto più efficienti dal punto di vista energetico.

---

### 5. Robustezza al Rumore Classico e Quantistico
Valutiamo la robustezza della strategia di controllo ottimizzata di Fig. 2 sia contro il rumore classico sul campo di pilotaggio, sia contro il rumore quantistico dovuto all'accoppiamento con un ambiente esterno termico 🔍 [Scheda 7](#scheda-7-rumore-di-controllo-ed-equazione-master-di-lindblad-gkls-con-bagno-ohmico).

#### A. Rumore Classico di Controllo
Consideriamo due modelli di rumore additivo $\Omega_D(t) \to \Omega_D(t) + \delta\Omega_D(t)$:
1. **Rumore bianco**: $\delta\Omega_D(t) = \gamma \xi(t)$, processo gaussiano non correlato a media nulla e varianza unitaria.
2. **Rumore colorato**: $\delta\Omega_D(t) = \gamma \tilde{\xi}(t)$, ottenuto filtrando il rumore bianco con un kernel gaussiano $G_{\tau_c}$ con tempo di correlazione $\tau_c = \tau_s / 3$, cioè un processo a banda finita $\tilde{\xi}(t) = (\xi * G_{\tau_c})(t)$.

Il parametro $\gamma$ quantifica l'ampiezza del rumore. Mediando su 100 realizzazioni stocastiche per ogni $\gamma$ [Fig. 4(a)]:
* Il protocollo rimane altamente robusto per entrambi i modelli, mantenendo $F \gtrsim 0.95$ fino a $\gamma/\omega_c \sim 0.1$ per il rumore bianco, e fino a $\gamma/\omega_c \sim 0.2$ per il rumore colorato.
* La maggiore robustezza al rumore colorato si spiega con la natura a banda larga del rumore bianco, le cui componenti ad alta frequenza disturbano più efficacemente le risonanze della dinamica.

#### B. Rumore Quantistico (Ambiente Termico)
Accoppiamo il sistema cavità-qubit a un ambiente bosonico termico a temperatura inversa $\beta = 1/(k_B T_{\text{env}})$. L'ambiente è modellato come un bagno di oscillatori armonici con densità spettrale Ohmica con cutoff esponenziale:
$$J(\omega) = \eta |\omega| e^{-|\omega|/\omega_B}$$
dove $\eta$ è la costante di accoppiamento sistema-bagno e $\omega_B$ è la frequenza di cutoff del bagno.

La dinamica del sistema ridotto è descritta nel formalismo di Gorini–Kossakowski–Lindblad–Sudarshan (GKLS) [40–42], valido nell'ipotesi di accoppiamento debole e dinamica markoviana:
$$\frac{d}{dt}\rho_S(t) = -i[H_S(t), \rho_S(t)] + \sum_\omega \left( L_\omega(t) \rho_S(t) L_\omega^\dagger(t) - \frac{1}{2} \{L_\omega^\dagger(t) L_\omega(t), \rho_S(t)\} \right) \quad \text{(Eq. 5)}$$
dove gli operatori di Lindblad $L_\omega(t)$ tengono conto dei canali dissipativi agenti sulla cavità o sul qubit.

I risultati [Fig. 4(b)] mostrano che:
* La fedeltà rimane elevata ($F \gtrsim 0.9$) fino a $\eta \lesssim 10^{-4}$.
* **Il rumore sul qubit è tollerato molto meglio del rumore sulla cavità**: la curva di fedeltà per dissipazione sul qubit decade molto più lentamente rispetto a quella per perdite di cavità.
* Alla soglia tipica di dispositivi superconduttori contemporanei $\eta = 10^{-4}$, la fedeltà dello stato finale $|n=6\rangle$ è $F = 0.901$ (contro $0.995$ del caso unitario), e la funzione di Wigner [Fig. 2(e)] preserva chiaramente i pattern di interferenza non-classici.

---

### 6. Conclusioni e Discussione
Abbiamo dimostrato che l'effetto Casimir dinamico in un sistema cavità-qubit operante nel regime USC può essere sfruttato per la generazione ad alta fedeltà di stati non-classici di cavità. Mediante il controllo ottimo, progettiamo protocolli che modulano la frequenza del qubit convertendo le fluttuazioni del vuoto in eccitazioni controllabili. La strategia ibrida gestisce in modo naturale vincoli di ampiezza, limitando la potenza di controllo complessiva.

La generazione di stati di Fock $|n\rangle$ raggiunge fedeltà superiori a $0.99$ fino a $n = 10$, rimanendo robusta contro rumore classico e dissipazione. L'approccio si estende a stati *squeezed* e stati gatto di Schrödinger. Il protocollo è realizzabile con l'attuale tecnologia a microonde in circuit-QED [45], opera su scale temporali notevolmente più brevi rispetto a quelle del regime di accoppiamento debole, e non richiede schemi di misura ed eraldatura (*heralded*), essendo intrinsecamente deterministico.

> [!IMPORTANT]
> **Collegamento con il tuo progetto di stage (Dall'articolo alle 2 Qubit):**
> L'ultima frase del paper dichiara esplicitamente:
> *"More broadly, extending the optimal-control framework developed here to multi-qubit cavity architectures may open new avenues for scalable quantum-state engineering."*
> **Questo è esattamente il cuore del tuo stage!** Estendere questa formulazione da 1 a 2 qubit nella cavità per scoprire se la cooperatività, la suddivisione del drive e la modulazione congiunta riducono il costo energetico $C^2$ e facilitano l'attuazione fisica in laboratorio.

---

### Appendice A: Generazione di Stati Squeezed
Lo stato di vuoto *squeezed* a singolo modo è definito come $S(r, \theta)|0\rangle$, dove l'operatore di squeezing è:
$$S(r, \theta) = \exp\left[ \frac{1}{2} r \left(e^{-i\theta} a^2 - e^{i\theta} a^{\dagger 2}\right) \right] \quad \text{(Eq. A1)}$$
con $r \ge 0$ intensità di squeezing e $\theta$ angolo nello spazio delle fasi 🔍 [Scheda 8](#scheda-8-stati-squeezed-e-misura-in-decibel-db). La varianza della quadratura compressa è $\Delta X^2 = \frac{1}{2} e^{-2r}$ (rispetto al vuoto $\Delta X_0^2 = 1/2$). In decibel:
$$r_{\text{dB}} = -10 \log_{10} \frac{\Delta X^2}{\Delta X_0^2} = 20 r \log_{10}(e) \implies r \approx \frac{r_{\text{dB}}}{8.686} \quad \text{(Eq. A2)}$$

* Per $r_{\text{dB}} = 3$ dB e $\theta = \pi/4$, la pipeline CRAB + GRAPE raggiunge una fedeltà straordinaria di **$F \simeq 0.999$** [Fig. 5(a,c,d)].
* Esplorando valori sperimentali $r_{\text{dB}} \in [0, 16]$ dB [Fig. 6(a,b)], per squeezing debole/moderato si mantiene $F \gtrsim 0.98$. A valori elevati di $r$, la convergenza richiede campi di controllo più strutturati, ma il raffinamento GRAPE abbatte drasticamente il costo energetico a parità di fedeltà.

---

### Appendice B: Generazione di Superposizioni di Stati Gatto di Schrödinger
I gatti di Schrödinger a due componenti sono sovrapposizioni di stati coerenti $|\pm\alpha\rangle$ ($a|\alpha\rangle = \alpha|\alpha\rangle$):
$$C_\alpha^\pm \propto |\alpha\rangle \pm |-\alpha\rangle \quad \text{(Eq. B3)}$$
Il paper affronta un benchmark ancora più esigente: una **sovrapposizione di stati cat lungo due assi ortogonali** dello spazio delle fasi 🔍 [Scheda 9](#scheda-9-stati-gatto-di-schrödinger-e-sovrapposizioni-su-assi-ortogonali):
$$|\psi_{\text{target}}\rangle = \mathcal{N} \left( C_\alpha^+ - C_{i\alpha}^+ \right) \quad \text{(Eq. B4)}$$
con $\alpha \in \mathbb{R}$. Questo stato presenta un caratteristico pattern a scacchiera di frange positive e negative al centro della funzione di Wigner, rendendolo ultra-sensibile a qualsiasi perdita di coerenza.

* Per $\alpha = 2$ (ogni componente coerente ha una media di $|\alpha|^2 = 4$ fotoni), il protocollo raggiunge una fedeltà finale di **$F = 0.978$** [Fig. 5(b,e,f)].
* Lo scaling con $\alpha \in [1, 3]$ [Fig. 6(c,d)] mostra $F \gtrsim 0.95$ per $\alpha < 3$. Anche qui GRAPE con vincoli riduce drasticamente l'energia del segnale.

---

# Parte 2 — Schede Didattiche di Approfondimento Fisico

---

### Scheda 1: Dal Modello di Jaynes-Cummings al Modello di Rabi e al Regime Ultrastro (USC)

#### 1. Il contesto: Circuit QED
Nell'elettrodinamica quantistica dei circuiti, una cavità a microonde (un risonatore a guida d'onda coplanare o LC) è accoppiata a un atomo artificiale (un qubit superconduttore come transmon o flux qubit).
* L'oscillatore armonico (la cavità) è descritto da:
  $$H_{\text{cav}} = \omega_c \left(a^\dagger a + \frac{1}{2}\right)$$
* Il qubit è descritto da due livelli energetici $\{|g\rangle, |e\rangle\}$ separati da un salto energetico $\omega_q$:
  $$H_{\text{qubit}} = \frac{\omega_q}{2} \sigma_z$$

#### 2. L'interazione dipolare e l'Hamiltoniana di Rabi
L'interazione tra la tensione del risonatore (proporzionale a $a + a^\dagger$) e la corrente/carica del qubit (proporzionale a $\sigma_x = \sigma_+ + \sigma_-$) è descritta dall'accoppiamento di dipolo 🔍 [Vedi derivazione completa nel Q&A #1](#qa-1--origine-fisica-delle-proporzionalità-di-tensione-e-caricadipolo):
$$H_{\text{int}} = g (a + a^\dagger)(\sigma_+ + \sigma_-) = g (a \sigma_+ + a^\dagger \sigma_- + a \sigma_- + a^\dagger \sigma_+)$$
Sommando i termini si ottiene l'**Hamiltoniana di Rabi completa**:
$$H_R = \omega_c a^\dagger a + \frac{\omega_q}{2} \sigma_z + g(a + a^\dagger)(\sigma_+ + \sigma_-)$$

#### 3. L'approssimazione d'onda rotante (RWA) e Jaynes-Cummings
Passando nel quadro di interazione (*interaction picture*) rispetto all'Hamiltoniana imperturbata $H_0 = \omega_c a^\dagger a + \frac{\omega_q}{2}\sigma_z$, gli operatori oscillano nel tempo come:
$$a(t) = a e^{-i\omega_c t}, \quad a^\dagger(t) = a^\dagger e^{+i\omega_c t}, \quad \sigma_-(t) = \sigma_- e^{-i\omega_q t}, \quad \sigma_+(t) = \sigma_+ e^{+i\omega_q t}$$
I quattro termini dell'interazione diventano:
1. $a \sigma_+ \propto e^{i(\omega_q - \omega_c)t}$ $\to$ **quasi-risonante** (se $\omega_q \approx \omega_c$, oscilla lentamente).
2. $a^\dagger \sigma_- \propto e^{-i(\omega_q - \omega_c)t}$ $\to$ **quasi-risonante**.
3. $a \sigma_- \propto e^{-i(\omega_q + \omega_c)t}$ $\to$ **contro-rotante** (oscilla a frequenza altissima $\approx 2\omega_c$).
4. $a^\dagger \sigma_+ \propto e^{+i(\omega_q + \omega_c)t}$ $\to$ **contro-rotante** (oscilla a frequenza altissima $\approx 2\omega_c$).

Se l'accoppiamento è debole ($g \ll \omega_c$), i termini ad alta frequenza mediano a zero rapidamente nel tempo e possono essere trascurati (**Rotating Wave Approximation, RWA**). Si ottiene la celebre **Hamiltoniana di Jaynes-Cummings (JC)**:
$$H_{JC} = \omega_c a^\dagger a + \frac{\omega_q}{2} \sigma_z + g(a \sigma_+ + a^\dagger \sigma_-)$$

#### 4. Perché nel regime USC la RWA crolla?
Quando il rapporto $g/\omega_c \gtrsim 0.1$ (nel paper $g/\omega_c = 0.3$), la forza di accoppiamento è talmente grande che la dinamica indotta da $g$ avviene su tempi comparabili al periodo di oscillazione dei termini contro-rotanti $\sim 1/(2\omega_c)$. I termini contro-rotanti **non possono più essere trascurati**: la RWA fallisce e bisogna usare il modello di Rabi completo.

---

### Scheda 2: Termini Contro-Rotanti ed Effetto Casimir Dinamico (DCE) Parametrico

#### 1. Cosa fanno fisicamente i termini contro-rotanti?
Guardiamo l'effetto dei singoli operatori sullo stato:
* Termini rotanti ($a \sigma_+$ e $a^\dagger \sigma_-$):
  $$a^\dagger \sigma_- |n, e\rangle \propto |n+1, g\rangle \quad \text{(un'eccitazione passa dal qubit alla cavità)}$$
  $$a \sigma_+ |n+1, g\rangle \propto |n, e\rangle \quad \text{(un fotone viene assorbito e il qubit si eccita)}$$
  In entrambi i casi, il numero totale di eccitazioni $n_{\text{ex}} = a^\dagger a + \sigma_+\sigma_-$ **si conserva**.
* Termini contro-rotanti ($a \sigma_-$ e $a^\dagger \sigma_+$):
  $$a \sigma_- |n, e\rangle \propto |n-1, g\rangle \quad \text{(distruzione simultanea di un fotone e di un'eccitazione del qubit: } \Delta n_{\text{ex}} = -2\text{)}$$
  $$a^\dagger \sigma_+ |n, g\rangle \propto |n+1, e\rangle \quad \text{(creazione simultanea di un fotone e di un'eccitazione del qubit: } \Delta n_{\text{ex}} = +2\text{)}$$
  Applicando $a^\dagger \sigma_+$ al vuoto quantistico $|0, g\rangle$, otteniamo lo stato $|1, e\rangle \neq 0$!

#### 2. L'Effetto Casimir Dinamico: dalle origini al circuito
* **Effetto Casimir Statico (1948)**: due specchi metallici neutri nel vuoto si attraggono a causa della modifica delle fluttuazioni di punto zero del campo elettromagnetico.
* **Effetto Casimir Dinamico originale (Moore 1970)**: se uno specchio viene fatto oscillare a velocità relativistiche prossime a $c$, le fluttuazioni del vuoto vengono convertite in fotoni reali emessi nello spazio. Muovere meccanicamente uno specchio a frequenze di gigahertz è quasi impossibile.
* **DCE Parametrico in Circuit QED**: invece di muovere uno specchio, si modula temporalmente una condizione al contorno o la frequenza di risonanza di un elemento quantistico accoppiato (il qubit o uno SQUID) a frequenza $\sim 2\omega_c$. In questo modo, la modulazione parametrica pompa energia nel vuoto, estraendo coppie reali di fotoni senza alcuna parte in movimento meccanico.

---

### Scheda 3: La Conservazione della Parità e le Regole di Selezione

#### 1. Definizione dell'operatore di Parità
Nello spazio congiunto cavità $\otimes$ qubit, l'operatore di parità è definito come:
$$\Pi = \exp(i\pi n_{\text{ex}}) = \exp[i\pi (a^\dagger a + \sigma_+ \sigma_-)]$$
Poiché $\sigma_+ \sigma_- = \frac{\mathbb{I} + \sigma_z}{2}$ ha autovalori $0$ (per $|g\rangle$) e $1$ (per $|e\rangle$), e $e^{i\pi a^\dagger a} = (-1)^n$ sullo stato di Fock $|n\rangle$, l'operatore si può scrivere anche come:
$$\Pi = -\sigma_z e^{i\pi a^\dagger a}$$

#### 2. Dimostrazione della simmetria $[\Pi, H_S(t)] = 0$
Verifichiamo come $\Pi$ agisce sui singoli operatori:
$$\Pi a \Pi^\dagger = -a, \quad \Pi a^\dagger \Pi^\dagger = -a^\dagger$$
$$\Pi \sigma_\pm \Pi^\dagger = -\sigma_\pm, \quad \Pi \sigma_z \Pi^\dagger = +\sigma_z$$
Ne consegue che:
* $a^\dagger a \to (-a^\dagger)(-a) = a^\dagger a$ (invariante)
* $\sigma_z \to \sigma_z$ (invariante)
* $(a + a^\dagger)(\sigma_+ + \sigma_-) \to [-(a + a^\dagger)][-(\sigma_+ + \sigma_-)] = +(a + a^\dagger)(\sigma_+ + \sigma_-)$ (invariante!)
Quindi sia $H_R$ sia $H_D(t) \propto \sigma_z$ commutano rigorosamente con $\Pi$:
$$[\Pi, H_R] = 0, \quad [\Pi, H_D(t)] = 0 \implies \frac{d\langle\Pi\rangle}{dt} = 0$$

#### 3. Regole di selezione per lo stato iniziale $|0, g\rangle$
Calcoliamo la parità dello stato iniziale:
$$\Pi |0, g\rangle = (-\sigma_z e^{i\pi a^\dagger a}) |0, g\rangle = -(-1)(+1) |0, g\rangle = +1 |0, g\rangle$$
Lo stato iniziale ha **parità $+1$ (pari)**.  
Dato che la parità è rigorosamente conservata per ogni $t$:
* Qualsiasi stato raggiungibile $|\psi(t)\rangle$ deve avere parità totale $+1$.
* Quando il qubit si ritrova nello stato $|g\rangle$, il campo di cavità può avere solo fotoni pari:
  $$\text{stati accessibili: } |0, g\rangle, |2, g\rangle, |4, g\rangle, |6, g\rangle, \dots$$
* Se volessimo preparare uno stato di Fock dispari (es. $|1\rangle, |3\rangle$), dovremmo o partire da uno stato iniziale dispari (es. $|0, e\rangle$), oppure rompere la parità con un termine asimmetrico nel drive (es. un drive su $\sigma_x$).

---

### Scheda 4: Metodi di Controllo Ottimo: CRAB vs GRAPE vs Interpolazione PCHIP

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PIPELINE IBRIDA DI CONTROLLO OTTIMO                  │
├─────────────────────┬───────────────────────┬──────────────────────────┤
│   Fase 1: CRAB      │     Fase 2: GRAPE     │  Fase 3: Interpolazione  │
│  (Esplorazione      │    (Raffinamento      │    (Fattibilità          │
│   Globale)          │     Locale)           │     Sperimentale)        │
│                     │                       │                          │
│  • Gradient-free    │  • Gradient-based     │  • Spline PCHIP          │
│  • Nelder-Mead      │  • L-BFGS-B           │  • Da gradini a liscio   │
│  • Fourier troncat. │  • Vincoli ampiezza   │  • Senza perdita         │
│  • Multi-seed (10x) │  • Trova il minimo    │    di fedeltà            │
│                     │    locale perfetto    │                          │
└─────────────────────┴───────────────────────┴──────────────────────────┘
```

#### 1. CRAB (Chopped Random Basis)
* **Idea**: invece di ottimizzare il valore del campo in ogni singolo istante $t$ (che darebbe centinaia di parametri indipendenti), si esprime il polso come somma di $N_f$ componenti di Fourier con frequenze estratte casualmente $\{\omega_k\}$:
  $$\Omega_D(t) = s(t) \sum_{k=1}^{N_f} [A_k \sin(\omega_k t) + B_k \cos(\omega_k t)]$$
* **Boundary function**: $s(t) = (1 - e^{-(t/\sigma)^2})(1 - e^{-((t-T)/\sigma)^2})$ forza $\Omega_D(0) = \Omega_D(T) = 0$, evitando shock non-fisici all'accensione e spegnimento.
* **Ottimizzatore**: usa l'algoritmo del simplesso di Nelder-Mead su $2 \times N_f$ parametri. È un metodo *gradient-free*: valuta solo la funzione di costo risolvendo l'equazione di Schrödinger con `sesolve`.
* **Perché serve**: è eccellente per esplorare globalmente il *landscape* senza rimanere intrappolato immediatamente nei minimi locali superficiali.

#### 2. GRAPE (Gradient Ascent Pulse Engineering)
* **Idea**: discretizza il tempo in intervalli costanti $\delta t$. Il controllo è un vettore di ampiezze costanti a tratti $u_j = \Omega_D(t_j)$.
* **Propagazione e Gradiente Analitico**: per ogni step temporale, l'evoluzione è data dall'operatore unitario $U_j = \exp(-i H(u_j) \delta t)$.
  La derivata esatta della fedeltà rispetto al controllo $u_j$ al tempo $j$ si calcola analiticamente senza differenze finite tramite il commutatore:
  $$\frac{\partial F}{\partial u_j} = -\text{Re}\left\{ \text{Tr}\left[ \lambda_j^\dagger \left( i \delta t [H_{\text{ctrl}}, \rho_j] \right) \right] \right\}$$
  dove $\rho_j$ è propagato in avanti da $t=0$, e $\lambda_j$ è il target propagato all'indietro da $t=T$.
* **Algoritmo L-BFGS-B**: sfrutta i gradienti esatti e costruisce un'approssimazione quasi-Newton dell'Hessiano, imponendo vincoli rigidi (*bounds*) sulle ampiezze consentite $u_{\text{min}} \le u_j \le u_{\text{max}}$.
* **Perché serve**: partendo dalla soluzione CRAB, GRAPE scende con precisione estrema nel minimo locale, aumentando la fedeltà (es. da 0.96 a 0.995) e contemporaneamente tagliando le ampiezze inutili.

#### 3. Interpolazione PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)
I generatori di forme d'onda arbitrari (AWG) di laboratorio non gradiscono segnali a gradino con derivate infinite. PCHIP crea una curva liscia $\mathcal{C}^1$ che passa per i punti GRAPE senza oscillazioni spurie (evita il fenomeno di Runge/Gibbs delle spline ordinarie).

---

### Scheda 5: Funzionale di Costo Energetico $C^2$ e Vincoli di Fattibilità Sperimentale

#### 1. Definizione e significato fisico
Nel paper, il costo energetico del controllo è definito come:
$$C^2(t) = \int_0^t ds \, \|H_D(s)\|_2^2 = \int_0^t ds \, \text{Tr}[H_D(s)^\dagger H_D(s)]$$
Poiché $H_D(t) = \frac{\Omega_D(t)}{2}\sigma_z$, calcolando la traccia su $\sigma_z^2 = \mathbb{I}_2$:
$$\text{Tr}\left[\left(\frac{\Omega_D(t)}{2}\sigma_z\right)^2\right] \propto \Omega_D(t)^2$$
Quindi il funzionale $C^2$ misura l'**energia totale integrata del segnale di pilotaggio**:
$$C^2 \approx \sum_{j} \Omega_D(t_j)^2 \delta t$$

#### 2. Perché è cruciale minimizzare $C^2$ in laboratorio?
1. **Riscaldamento**: correnti e tensioni a microonde elevate nei cavi coassiali criogenici introducono calore nel criostato a diluizione (che opera a $\sim 15$ mK).
2. **Uscita dal modello a 2 livelli**: i qubit reali (es. transmon) sono oscillatori debolmente anarmonici. Se il drive $\Omega_D(t)$ è troppo intenso, il sistema salta al secondo stato eccitato $|f\rangle$ o si ionizza, distruggendo la computazione.
3. **Banda passante dell'elettronica**: segnali ad ampiezza estrema o con frequenze troppo alte superano i limiti di saturazione degli amplificatori criogenici e dei convertitori DAC.

---

### Scheda 6: La Funzione di Wigner e la Negatività nello Spazio delle Fasi

#### 1. Definizione matematica
La funzione di Wigner $W(x, p)$ è una quasi-distribuzione di probabilità nello spazio delle fasi quantistico $(x, p)$, introdotta da Eugene Wigner nel 1932:
$$W(x, p) = \frac{1}{\pi\hbar} \int_{-\infty}^{+\infty} dy \, \langle x - y | \rho | x + y \rangle e^{2i p y / \hbar}$$
dove $x = \frac{a + a^\dagger}{\sqrt{2}}$ e $p = \frac{a - a^\dagger}{i\sqrt{2}}$ sono gli operatori di quadratura del campo di cavità.

#### 2. Proprietà chiave
* Integrata su tutto lo spazio dà 1: $\iint W(x, p) dx dp = 1$.
* Integrata su $p$ fornisce la densità di probabilità spaziale: $\int W(x, p) dp = |\psi(x)|^2$.
* Integrata su $x$ fornisce la densità di probabilità del momento: $\int W(x, p) dx = |\phi(p)|^2$.

#### 3. Il Teorema di Hudson e la Negatività
A differenza di una vera distribuzione di probabilità classica, **la funzione di Wigner può assumere valori negativi**:
* **Teorema di Hudson (1974)**: gli unici stati quantistici puri la cui funzione di Wigner è ovunque positiva ($W(x,p) \ge 0$) sono gli stati gaussiani (stato fondamentale, stati coerenti, stati termici).
* Se $W(x, p) < 0$ in qualche regione, lo stato è **inequivocabilmente non-classico**. La negatività è una misura diretta di interferenza quantistica nello spazio delle fasi.
* Negli stati di Fock $|n\rangle$, $W(x, p)$ presenta $n$ anelli concentrici che alternano valori positivi e negativi. Nel punto centrale $(0,0)$:
  $$W(0, 0) = \frac{(-1)^n}{\pi}$$
  Per $n=6$, $W(0,0) > 0$, ma è circondato da anelli con forte negatività (come ben visibile in Fig. 2c-e).

---

### Scheda 7: Rumore di Controllo ed Equazione Master di Lindblad (GKLS) con Bagno Ohmico

#### 1. Perché l'equazione di Schrödinger non basta più
In un setup reale, il sistema non è isolato: la cavità perde fotoni attraverso le pareti o la linea di trasmissione, e il qubit subisce dephasing e rilassamento energetico dovuto a difetti del substrato e fluttuazioni di carica/flusso. L'evoluzione non è più unitaria ma aperta, descritta dalla matrice densità $\rho(t)$.

#### 2. L'Equazione Master GKLS
$$\frac{d\rho_S}{dt} = -i[H_S(t), \rho_S(t)] + \sum_\omega \mathcal{D}[L_\omega]\rho_S(t)$$
con il superoperatore dissipativo di Lindblad:
$$\mathcal{D}[L]\rho = L \rho L^\dagger - \frac{1}{2} \{L^\dagger L, \rho\}$$
* Nel regime USC, poiché $g$ è grande, la derivazione microscopica dei salti quantici va fatta nella **base degli autostati dell'Hamiltoniana accoppiata** (formalismo di Beaudoin-Gambetta-Blais 2011), altrimenti si incorre in paradossi non-fisici come l'emissione spontanea dal vuoto!

#### 3. Perché il sistema è più sensibile alle perdite di cavità rispetto al qubit?
Nel nostro protocollo, i fotoni vengono creati per rimanere nella cavità (stati target ad alto numero di fotoni, es. $|n=6\rangle$).
* La perdita di un singolo fotone da parte di una cavità in $|n=6\rangle$ scala con $n \kappa = 6 \kappa$, degradando immediatamente l'overlap con lo stato target (la fedeltà crolla a zero se si perde un fotone, poiché $\langle 5|6\rangle = 0$).
* Il qubit, al contrario, agisce come "catalizzatore": viene modulato per trasferire eccitazioni, ma a fine protocollo ritorna vicino al suo stato fondamentale $|g\rangle$. Pertanto, le fluttuazioni sul qubit hanno un impatto meno distruttivo rispetto alla fuga di fotoni dalla cavità.

---

### Scheda 8: Stati Squeezed e Misura in Decibel (dB)

#### 1. Definizione dell'operatore di Squeezing
$$S(r, \theta) = \exp\left[ \frac{1}{2} r \left(e^{-i\theta} a^2 - e^{i\theta} a^{\dagger 2}\right) \right]$$
Agendo sull'operatore di distruzione, produce la trasformazione di Bogoliubov:
$$S^\dagger a S = a \cosh(r) - a^\dagger e^{i\theta} \sinh(r)$$

#### 2. Riduzione dell'incertezza sotto il limite quantistico standard
Definendo le quadrature ruotate di un angolo $\theta/2$:
$$\Delta X_1^2 = \frac{1}{2} e^{-2r}, \quad \Delta X_2^2 = \frac{1}{2} e^{+2r} \implies \Delta X_1 \Delta X_2 = \frac{1}{4}$$
Il prodotto delle indeterminazioni satura il principio di indeterminazione di Heisenberg, ma le fluttuazioni lungo la direzione 1 sono compresse sotto il livello del vuoto ($1/2$).

#### 3. Relazione tra $r$ e i Decibel (dB)
Nei laboratori sperimentali, la riduzione di rumore rispetto al vuoto si esprime su scala logaritmica:
$$r_{\text{dB}} = -10 \log_{10}\left(\frac{\Delta X_1^2}{\Delta X_{\text{vacuum}}^2}\right) = -10 \log_{10}(e^{-2r}) = 20 r \log_{10}(e) \approx 8.686 \times r$$
* Esempio: $3\text{ dB}$ di squeezing corrispondono a $r \approx 3 / 8.686 \approx 0.345$, ovvero un dimezzamento del rumore in potenza ($\Delta X^2 / \Delta X_0^2 = 10^{-0.3} \approx 0.5$).
* Uno squeezing di $10\text{ dB}$ riduce la varianza di un fattore 10 ($r \approx 1.15$).

---

### Scheda 9: Stati Gatto di Schrödinger e Sovrapposizioni su Assi Ortogonali

#### 1. Stato Coerente vs Stato Gatto
* Uno stato coerente $|\alpha\rangle = e^{-|\alpha|^2/2}\sum_{n=0}^\infty \frac{\alpha^n}{\sqrt{n!}}|n\rangle$ è lo stato quantistico più simile a un'onda classica (spostamento del vuoto nello spazio delle fasi).
* Uno stato gatto di Schrödinger è una sovrapposizione coerente di due stati macroscopici distinti (es. "vivo" $|\alpha\rangle$ e "morto" $|-\alpha\rangle$):
  $$|C_\alpha^+\rangle \propto |\alpha\rangle + |-\alpha\rangle \quad \text{(even cat)}$$
  Contiene solo componenti con numero pari di fotoni.

#### 2. Il Target del Paper: Cat su Assi Ortogonali (Eq. B4)
Il paper sceglie uno stato bersaglio ancora più ricco:
$$|\psi_{\text{target}}\rangle \propto C_\alpha^+ - C_{i\alpha}^+ \propto (|\alpha\rangle + |-\alpha\rangle) - (|i\alpha\rangle + |-i\alpha\rangle)$$
I quattro stati coerenti formano una croce simmetrica nel piano complesso a distanza $\alpha$ dall'origine.
* Al centro dello spazio delle fasi si genera una fitta griglia di interferenza quantistica a scacchiera (*checkerboard pattern*).
* Questo stato è di enorme interesse per i codici di correzione d'errore quantistico bosonico (come i codici cat e binomiali), poiché protegge l'informazione quantistica contro le perdite di fotoni.

---

# Parte 3 — Registro Approfondimenti su Richiesta (Q&A)

> In questa sezione vengono inseriti tutti gli approfondimenti, le derivazioni matematiche e i chiarimenti fisici richiesti durante lo studio del paper.

---

### Q&A #1 — Origine Fisica delle Proporzionalità di Tensione e Carica/Dipolo

**Domanda:**  
*Da dove arrivano le proporzionalità della tensione del risonatore con $(a + a^\dagger)$ e della carica/corrente del qubit con $\sigma_x = \sigma_+ + \sigma_-$ nell'interazione di dipolo?*

---

#### 1. Perché la Tensione del Risonatore è proporzionale a $(a + a^\dagger)$?

In Circuit QED, una cavità elettromagnetica (o un risonatore a microonde) è descritta come un **circuito LC risonante**.

##### A. Il parallelo con l'oscillatore armonico meccanico
Ricordiamo che per una massa su una molla:
* Coordinata di posizione $\hat{x} = x_{\text{zpf}} (a + a^\dagger)$, dove $x_{\text{zpf}} = \sqrt{\frac{\hbar}{2m\omega}}$ rappresenta le fluttuazioni quantistiche di punto zero (*zero-point fluctuations*).
* Momento coniugato $\hat{p} = -i p_{\text{zpf}} (a - a^\dagger)$, con $[\hat{x}, \hat{p}] = i\hbar$.
* L'Hamiltoniana è $H = \frac{\hat{p}^2}{2m} + \frac{1}{2}m\omega^2 \hat{x}^2 = \hbar\omega \left(a^\dagger a + \frac{1}{2}\right)$.

##### B. Quantizzazione del circuito LC
In un circuito LC ideale con induttanza $L$ e capacità $C$, l'energia classica immagazzinata è la somma dell'energia elettrostatica nel condensatore e di quella magnetica nell'induttore:
$$H = \frac{Q^2}{2C} + \frac{\Phi^2}{2L}$$
dove $Q$ è la carica sulle armature del condensatore e $\Phi = \int V(t) dt$ è il flusso magnetico concatenato all'induttore.

Esiste un'equivalenza esatta tra le variabili meccaniche e circuitali:
$$\text{Coordinata: } \hat{x} \longleftrightarrow \hat{Q} \quad (\text{oppure } \hat{\Phi})$$
$$\text{Momento: } \hat{p} \longleftrightarrow \hat{\Phi} \quad (\text{oppure } \hat{Q})$$
$$\text{Massa: } m \longleftrightarrow C$$
$$\text{Frequenza di risonanza: } \omega_c = \frac{1}{\sqrt{LC}}$$

Imponendo la regola di commutazione canonica $[\hat{\Phi}, \hat{Q}] = i\hbar$, definiamo gli operatori di scala $a$ e $a^\dagger$:
$$\hat{Q} = Q_{\text{zpf}} (a + a^\dagger) \quad \text{con} \quad Q_{\text{zpf}} = \sqrt{\frac{\hbar \omega_c C}{2}}$$
$$\hat{\Phi} = -i \Phi_{\text{zpf}} (a - a^\dagger) \quad \text{con} \quad \Phi_{\text{zpf}} = \sqrt{\frac{\hbar}{2 \omega_c C}}$$

##### C. La Tensione ai capi del risonatore
Dalla relazione fondamentale del condensatore $V = Q / C$, l'operatore di tensione quantizzato diventa:
$$\hat{V} = \frac{\hat{Q}}{C} = \frac{Q_{\text{zpf}}}{C} (a + a^\dagger) = V_{\text{zpf}} (a + a^\dagger)$$
dove:
$$V_{\text{zpf}} = \sqrt{\frac{\hbar \omega_c}{2C}}$$
rappresenta la **tensione di fluttuazione di punto zero** nel risonatore.

> **In sintesi:** Così come la posizione di una particella oscilla come $\hat{x} \propto (a + a^\dagger)$, la carica del condensatore e la tensione del risonatore sono le quadrature "di posizione" del campo elettromagnetico:
> $$\hat{V}_{\text{cav}} \propto (a + a^\dagger)$$
> (Nei risonatori distribuiti o cavità 3D, il campo elettrico locale $\hat{\mathbf{E}}(\mathbf{r})$ è proporzionale all'integrale di tensione e quindi a sua volta proporzionale a $a + a^\dagger$).

---

#### 2. Perché la Carica/Corrente del Qubit è proporzionale a $\sigma_x = \sigma_+ + \sigma_-$?

Consideriamo un atomo artificiale (come un transmon o Cooper-Pair Box) posizionato vicino al risonatore.

##### A. L'interazione fisica: accoppiamento capacitivo
Il qubit possiede un'isola superconduttrice caratterizzata dall'operatore carica:
$$\hat{Q}_q = 2e \hat{n}$$
dove $\hat{n}$ è l'operatore che conta il numero di coppie di Cooper in eccesso sull'isola, ed $e$ è la carica dell'elettrone.

Tra il campo di cavità (a potenziale $\hat{V}_{\text{cav}}$) e l'isola del qubit esiste una capacità di accoppiamento parassita $C_g$. L'energia di interazione elettrostatica corrisponde al lavoro necessario per portare carica sull'isola in presenza del potenziale della cavità:
$$H_{\text{int}} = \hat{Q}_q \cdot \beta \hat{V}_{\text{cav}} = 2e \beta \hat{V}_{\text{cav}} \hat{n}$$
(dove $\beta = C_g / C_{\Sigma} < 1$ è il rapporto di partizione capacitiva).  
Questo termine è formalmente identico all'interazione di dipolo elettrico atomica $-\hat{\mathbf{d}} \cdot \hat{\mathbf{E}}$, dove la carica/dipolo del sistema interagisce con il potenziale/campo esterno.

##### B. Proiezione dell'operatore carica sul sottospazio a due livelli $\{|g\rangle, |e\rangle\}$
Vogliamo capire che forma ha l'operatore carica $\hat{n}$ quando ci limitiamo ai due livelli più bassi del qubit (stato fondamentale $|g\rangle$ e primo eccitato $|e\rangle$):
$$\hat{n} \approx \begin{pmatrix} \langle g|\hat{n}|g\rangle & \langle g|\hat{n}|e\rangle \\ \langle e|\hat{n}|g\rangle & \langle e|\hat{n}|e\rangle \end{pmatrix}$$

1. **Parità del potenziale e delle funzioni d'onda:**
   L'Hamiltoniana del transmon è data da $H_q = 4E_C (\hat{n} - n_g)^2 - E_J \cos\hat{\phi}$, dove $\phi$ è la differenza di fase superconduttrice.
   Poiché il potenziale $-E_J \cos\phi$ è una funzione **PARI** rispetto a $\phi$ ($\phi \to -\phi$):
   * La funzione d'onda dello stato fondamentale $\psi_g(\phi) = \langle \phi|g\rangle$ è **PARI**: $\psi_g(-\phi) = +\psi_g(\phi)$.
   * La funzione d'onda del primo stato eccitato $\psi_e(\phi) = \langle \phi|e\rangle$ è **DISPARI**: $\psi_e(-\phi) = -\psi_e(\phi)$.

2. **Parità dell'operatore carica:**
   Nel formalismo canonico, la carica è il generatore delle traslazioni di fase:
   $$\hat{n} = -i \frac{\partial}{\partial \phi}$$
   La derivata prima è un operatore **DISPARI** rispetto all'inversione $\phi \to -\phi$.

3. **Calcolo degli elementi di matrice:**
   * **Elementi diagonali:**
     $$\langle g|\hat{n}|g\rangle = \int_{-\pi}^{+\pi} \underbrace{\psi_g^*(\phi)}_{\text{pari}} \underbrace{\left(-i\frac{\partial}{\partial\phi}\right)}_{\text{dispari}} \underbrace{\psi_g(\phi)}_{\text{pari}} d\phi = 0$$
     $$\langle e|\hat{n}|e\rangle = \int_{-\pi}^{+\pi} \underbrace{\psi_e^*(\phi)}_{\text{dispari}} \underbrace{\left(-i\frac{\partial}{\partial\phi}\right)}_{\text{dispari}} \underbrace{\psi_e(\phi)}_{\text{dispari}} d\phi = 0$$
     *Significato fisico:* né lo stato fondamentale né lo stato eccitato possiedono una carica o un momento di dipolo permanente statico. Il valore medio della carica è nullo in entrambi gli stati.
   * **Elementi fuori diagonale (elementi di transizione):**
     $$\langle e|\hat{n}|g\rangle = \int_{-\pi}^{+\pi} \underbrace{\psi_e^*(\phi)}_{\text{dispari}} \underbrace{\left(-i\frac{\partial}{\partial\phi}\right)}_{\text{dispari}} \underbrace{\psi_g(\phi)}_{\text{pari}} d\phi = n_{01} \neq 0$$
     L'integrando è il prodotto di tre termini con parità complessiva pari: l'integrale non è nullo!

4. **Forma matriciale:**
   Scegliendo opportunamente le fasi globali dei ket (in modo che $n_{01}$ sia reale):
   $$\hat{n} = \begin{pmatrix} 0 & n_{01} \\ n_{01} & 0 \end{pmatrix} = n_{01} \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = n_{01} \sigma_x$$
   Ricordando che per gli operatori di innalzamento e abbassamento:
   $$\sigma_+ = |e\rangle\langle g| = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}, \quad \sigma_- = |g\rangle\langle e| = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$$
   la matrice di Pauli $\sigma_x$ è esattamente:
   $$\sigma_x = \sigma_+ + \sigma_-$$

> **In sintesi:** La carica del qubit (o il dipolo elettrico di un atomo) non può connettere uno stato con se stesso (elementi diagonali nulli per parità), ma connette lo stato fondamentale con quello eccitato. Di conseguenza, nella base energetica $\{|g\rangle, |e\rangle\}$ ha solo componenti fuori-diagonale, che coincidono matematicamente con:
> $$\hat{Q}_q \propto \sigma_x = \sigma_+ + \sigma_-$$

---

#### 3. Conclusione: L'Hamiltoniana di Interazione di Rabi

Mettendo insieme i due risultati:
$$H_{\text{int}} = \beta \hat{V}_{\text{cav}} \cdot \hat{Q}_q = \left[ V_{\text{zpf}} (a + a^\dagger) \right] \cdot \left[ 2e \beta n_{01} (\sigma_+ + \sigma_-) \right]$$
Raggruppando tutte le costanti fisiche nella costante di accoppiamento luce-materia $g$:
$$g := 2e \beta V_{\text{zpf}} n_{01}$$
si ottiene rigorosamente la forma utilizzata nel paper:
$$H_{\text{int}} = g (a + a^\dagger)(\sigma_+ + \sigma_-) = g (a\sigma_+ + a^\dagger \sigma_- + a\sigma_- + a^\dagger \sigma_+)$$

---

### Q&A #2 — Gli Stati Non-Classici dell'Oscillatore Armonico nel Paper

**Domanda:**  
*Cosa sono gli stati non classici dell'oscillatore armonico citati nel paper (Fock, Squeezed, Gatti di Schrödinger)? In che senso sono "non classici" e perché sono così importanti?*

---

#### 1. Il confine tra "Classico" e "Quantistico" nell'Oscillatore Armonico

Per capire cosa rende uno stato *non classico*, dobbiamo prima definire qual è lo **stato più classico possibile** di un oscillatore armonico (o di un modo elettromagnetico di cavità).

##### A. Lo stato classico per eccellenza: lo Stato Coerente di Glauber $|\alpha\rangle$
Negli anni '60, Roy Glauber (premio Nobel nel 2005) dimostrò che gli stati quantistici che imitano più fedelmente un campo elettromagnetico classico (come la luce emessa da un laser ideale o un'oscillazione sinusoidale macroscopica) sono gli **stati coerenti** $|\alpha\rangle$:
* Sono gli autostati dell'operatore di distruzione: $a|\alpha\rangle = \alpha|\alpha\rangle$, con $\alpha = |\alpha|e^{i\phi} \in \mathbb{C}$.
* Hanno fluttuazioni di incertezza **minime e simmetriche** nello spazio delle fasi:
  $$\Delta X_1 = \Delta X_2 = \frac{1}{\sqrt{2}} \implies \Delta X_1 \Delta X_2 = \frac{1}{2}$$
  Nello spazio delle fasi $(x, p)$, uno stato coerente è rappresentato da un **cerchio di incertezza** identico a quello del vuoto $|0\rangle$, semplicemente traslato al punto $(\text{Re}\,\alpha, \text{Im}\,\alpha)$.
* La statistica dei fotoni è perfettamente **poissoniana**: la varianza del numero di fotoni è pari al valor medio:
  $$\langle n \rangle = |\alpha|^2, \quad \Delta n^2 = \langle n \rangle$$
* La loro funzione di Wigner è una **gaussiana bidimensionale ovunque positiva**: $W(x, p) \ge 0$.

##### B. Definizione rigorosa di "Non-Classicità"
Uno stato $\rho$ è definito **non classico** se non può essere descritto come una miscela statistica classica di stati coerenti.
I criteri fisici e matematici principali sono:

1. **Criterio di Glauber-Sudarshan**:  
   Se proviamo a scrivere la matrice densità come $\rho = \int P(\alpha) |\alpha\rangle\langle\alpha| d^2\alpha$, per uno stato non classico la funzione $P(\alpha)$ **non è una vera densità di probabilità**: assume valori negativi oppure diventa più singolare di una delta di Dirac (es. derivate di delta).
2. **Negatività della Funzione di Wigner ($W(x, p) < 0$)**:  
   Per il celebre **Teorema di Hudson (1974)**, gli *unici* stati quantistici puri la cui funzione di Wigner è ovunque non-negativa sono gli stati gaussiani (il vuoto, gli stati coerenti e gli stati termici).  
   Se la funzione di Wigner diventa negativa in qualche regione dello spazio delle fasi, lo stato è **inequivocabilmente non classico**: la negatività è la firma diretta di **interferenza quantistica nello spazio delle fasi**.
3. **Statistica sub-Poissoniana**:  
   Fluttuazioni del numero di fotoni inferiori al limite poissoniano ($\Delta n^2 < \langle n \rangle$). In termini del parametro di Mandel $Q = \frac{\Delta n^2 - \langle n \rangle}{\langle n \rangle}$:
   $$Q < 0 \implies \text{statistica sub-Poissoniana (impossibile nella fisica classica delle onde)}$$
4. **Squeezing delle quadrature**:  
   Fluttuazioni del campo lungo una direzione ridotte al di sotto del rumore quantistico di punto zero del vuoto ($\Delta X_1^2 < 1/2$).

---

#### 2. I Tre Stati Non-Classici Studiati nel Paper

Il paper si concentra sulla generazione deterministica di tre archetipi fondamentali di stati non-classici della cavità:

```
┌────────────────────────────────────────────────────────────────────────┐
│             I TRE TIPI DI STATI NON-CLASSICI DEL PAPER                 │
├────────────────────┬───────────────────────┬───────────────────────────┤
│ 1. STATI DI FOCK   │  2. STATI SQUEEZED    │ 3. GATTI DI SCHRÖDINGER   │
│    |n⟩             │     S(r, θ)|0⟩        │    |C_α^+⟩ - |C_{iα}^+⟩   │
├────────────────────┼───────────────────────┼───────────────────────────┤
│ • Numero fotoni    │ • Fluttuazioni di     │ • Sovrapposizione         │
│   esatto: Δn = 0   │   quadratura sotto    │   quantistica di stati    │
│ • Fase totalmente  │   il livello di vuoto │   coerenti distinti       │
│   indeterminata    │ • Coppie correlate di │ • Interferenza a          │
│ • Wigner con n     │   fotoni (DCE)        │   scacchiera              │
│   anelli negativi  │ • Ellisse in fase     │ • Codici di correzione    │
│ • Bosonic Qubit    │ • Metrologia (LIGO)   │   d'errore quantistico    │
└────────────────────┴───────────────────────┴───────────────────────────┘
```

---

#### A. Stati di Fock $|n\rangle$ (Autostati del Numero di Fotoni)

* **Definizione:**  
  Sono gli autostati dell'operatore numero di fotoni:
  $$a^\dagger a |n\rangle = n |n\rangle$$
  Rappresentano uno stato del campo che contiene *esattamente* $n$ quanti di energia.

* **Perché sono non-classici:**
  1. **Incertezza nulla sul numero di fotoni:** $\Delta n = 0$. Il parametro di Mandel è $Q = -1$ (il minimo valore teoricamente possibile, massima statistica sub-Poissoniana).
  2. **Indeterminazione totale di fase:** In meccanica quantistica vale la relazione di indeterminazione numero-fase $\Delta n \Delta \phi \ge \frac{1}{2}$. Se $\Delta n = 0$, la fase dell'onda $\phi$ è totalmente casuale e uniformemente distribuita su $[0, 2\pi)$. Non ha alcuna somiglianza con un'onda elettromagnetica classica.
  3. **Funzione di Wigner altamente non-gaussiana:**  
     La funzione di Wigner per lo stato di Fock $|n\rangle$ è a simmetria circolare (non dipende dalla fase) ed è data da:
     $$W_n(x, p) = \frac{(-1)^n}{\pi} e^{-(x^2 + p^2)} L_n(2(x^2 + p^2))$$
     dove $L_n$ sono i polinomi di Laguerre.  
     Essa presenta $n$ anelli concentrici che alternano valori positivi e fortemente negativi! Al centro dello spazio delle fasi $(0,0)$:
     $$W_n(0, 0) = \frac{(-1)^n}{\pi}$$
     Per $n=1, 3, 5\dots$ il centro è rigorosamente negativo; per $n=2, 4, 6\dots$ il centro è positivo ma è circondato da valli a valori fortemente negativi (come mostrato chiaramente in Fig. 2c-e del paper per $|n=6\rangle$).

* **Nel paper e nello stage:**  
  Il benchmark principale è la generazione dello stato $|n=6\rangle$ (e lo studio dello scaling fino a $n=10$) partendo dal vuoto $|0\rangle$, exploitando il DCE che genera eccitazioni a coppie.

---

#### B. Stati di Vuoto Squeezed $S(r, \theta)|0\rangle$ (Luce Compressa)

* **Definizione:**  
  Generati applicando al vuoto $|0\rangle$ l'operatore di squeezing quadratico:
  $$S(r, \theta) = \exp\left[ \frac{1}{2} r \left(e^{-i\theta} a^2 - e^{i\theta} a^{\dagger 2}\right) \right]$$
  dove $r \ge 0$ è l'ampiezza di squeezing e $\theta$ è l'angolo di orientazione nel piano delle fasi.

* **Perché sono non-classici:**
  1. **Compressione sotto il vuoto quantistico:**  
     Il principio di indeterminazione impone $\Delta X_1 \Delta X_2 \ge \frac{1}{2}$. Lo stato fondamentale (vuoto) distribuisce l'incertezza in modo isotropo: $\Delta X_1 = \Delta X_2 = \frac{1}{\sqrt{2}}$.  
     Uno stato *squeezed* redistribuisce l'incertezza comprimendo una quadratura al di sotto del limite fondamentale del vuoto:
     $$\Delta X_1 = \frac{1}{\sqrt{2}} e^{-r} < \frac{1}{\sqrt{2}}, \quad \Delta X_2 = \frac{1}{\sqrt{2}} e^{+r} > \frac{1}{\sqrt{2}}$$
     Il rumore su una misura di campo elettrico o ampiezza è inferiore al rumore del vuoto stesso!
  2. **Origine fisica (coppie di fotoni):**  
     L'operatore $a^{\dagger 2}$ crea fotoni rigorosamente a coppie. Lo stato di vuoto compresso contiene solo componenti pari dello spazio di Fock:
     $$S(r, 0)|0\rangle = \frac{1}{\sqrt{\cosh r}} \sum_{m=0}^\infty \frac{\sqrt{(2m)!}}{2^m m!} (\tanh r)^m |2m\rangle$$
     Questa correlazione quantistica a due fotoni è il motivo per cui l'Effetto Casimir Dinamico parametrico (che eccita termini contro-rotanti $a^{\dagger 2}$) è la sorgente naturale per eccellenza di stati *squeezed*!

* **Applicazioni:**  
  Nei rivelatori di onde gravitazionali come LIGO e Virgo, l'iniezione di luce *squeezed* nel braccio scuro dell'interferometro ha permesso di abbattere il rumore di conteggio dei fotoni (*shot noise*) aumentando la sensibilità astrofisica di oltre il 50%.

---

#### C. Stati Gatto di Schrödinger e Sovrapposizioni su Assi Ortogonali

* **Definizione del "Gatto" quantistico:**  
  Prende il nome dal celebre paradosso di Erwin Schrödinger (1935). Invece di un gatto macroscopico vivo e morto, in cavità si considera la sovrapposizione quantistica di due stati coerenti a fase opposta:
  $$|C_\alpha^\pm\rangle = \frac{1}{\sqrt{2(1 \pm e^{-2|\alpha|^2})}} \left( |\alpha\rangle \pm |-\alpha\rangle \right)$$
  Lo stato $|+\alpha\rangle$ e lo stato $|-\alpha\rangle$ hanno fasi opposte (distanza $2|\alpha|$ nello spazio delle fasi). Se $|\alpha|$ è grande (es. $|\alpha|=2 \implies |\alpha|^2 = 4$ fotoni medi), essi sono quasi ortogonali ($\langle -\alpha|\alpha\rangle = e^{-2|\alpha|^2} \ll 1$).

* **Miscela statistica classica vs Sovrapposizione quantistica:**
  * Se avessimo una situazione classica (incertezza per ignoranza), la matrice densità sarebbe una miscela al 50%:
    $$\rho_{\text{classica}} = \frac{1}{2}|\alpha\rangle\langle\alpha| + \frac{1}{2}|-\alpha\rangle\langle-\alpha|$$
    La sua funzione di Wigner mostra semplicemente due "montagnole" gaussiane separate in $\pm\alpha$, sempre positive.
  * In uno stato gatto puro, la matrice densità contiene i termini di coerenza quantistica fuori-diagonale:
    $$\rho_{\text{cat}} = \frac{1}{2}|\alpha\rangle\langle\alpha| + \frac{1}{2}|-\alpha\rangle\langle-\alpha| + \underbrace{\frac{1}{2}|\alpha\rangle\langle-\alpha| + \frac{1}{2}|-\alpha\rangle\langle\alpha|}_{\text{interferenza quantistica}}$$
    Questi termini incrociati creano nello spazio delle fasi, proprio a metà strada tra i due stati (all'origine $x=0, p=0$), delle **frange di interferenza con violenta negatività di Wigner**.

* **La Sovrapposizione su Assi Ortogonali del Paper (Eq. B4):**  
  Nel paper gli autori scelgono un bersaglio ancora più affascinante: una sovrapposizione di 4 stati coerenti disposti a croce sui due assi ortogonali (reale e immaginario) del piano complesso:
  $$|\psi_{\text{target}}\rangle \propto C_\alpha^+ - C_{i\alpha}^+ \propto (|\alpha\rangle + |-\alpha\rangle) - (|i\alpha\rangle + |-i\alpha\rangle)$$
  * L'interferenza tra le 4 componenti dà origine al centro della funzione di Wigner a un **motivo a scacchiera (*checkerboard pattern*)** con picchi positivi e minimi negativi alternati.
  * **Importanza tecnologica:** Questa classe di stati è alla base dei **Cat Codes** e dei **Bosonic Error-Correcting Codes** (sviluppati nei laboratori di Yale e circuit-QED). Poiché i fotoni nella cavità tendono a perdersi uno alla volta per dissipazione ($a$), l'azione dell'operatore $a$ trasforma un gatto pari in un gatto dispari senza distruggere la superposizione; misurando la parità della cavità è possibile rilevare e correggere l'errore senza distruggere l'informazione quantistica memorizzata!

---

### Q&A #3 — Gli Autostati $u_n(x)$ non sono gli "stati classici"? Il Paradosso degli Stati di Fock

**Domanda:**  
*Nella formula che ho studiato nel corso di Meccanica Quantistica:*
$$u_n(x) = \left(\frac{m\omega}{\pi\hbar}\right)^{1/4} \frac{1}{\sqrt{2^n n!}} H_n\left(\sqrt{\frac{m\omega}{\hbar}} x\right) e^{-\frac{m\omega x^2}{2\hbar}}$$
*questi sono gli stati dell'oscillatore armonico con i polinomi di Hermite $H_n$. Non sono questi gli "stati classici"? Perché diciamo che sono gli stati di Fock e che sono fortemente NON classici?*

---

#### 1. Cosa rappresentano esattamente le funzioni $u_n(x)$?

La formula dell'immagine è la **funzione d'onda nella rappresentazione delle posizioni degli STATI DI FOCK $|n\rangle$**:
$$u_n(x) = \langle x | n \rangle$$
Esiste una perfetta equivalenza tra i due linguaggi:
* Nel **linguaggio degli operatori di Dirac** (seconda quantizzazione): lo stato si scrive come ket $|n\rangle$, ottenuto applicando l'operatore di creazione al vuoto:
  $$|n\rangle = \frac{(a^\dagger)^n}{\sqrt{n!}} |0\rangle, \quad a^\dagger a |n\rangle = n |n\rangle$$
* Nel **linguaggio della funzione d'onda nello spazio reale** (prima quantizzazione di Schrödinger): lo stato è $\psi_n(x) = \langle x | n \rangle \equiv u_n(x)$.

Quindi **$u_n(x)$ e lo stato di Fock $|n\rangle$ sono esattamente lo stesso identico stato fisico**, espresso semplicemente in due rappresentazioni matematiche diverse!

---

#### 2. Perché nei corsi universitari si studiano per primi?

Nel corso di Meccanica Quantistica 1 / Istituzioni di Fisica Teorica, $u_n(x)$ è il **primo problema analitico** che si risolve perché sono gli **autostati dell'energia (stati stazionari)** dell'equazione di Schrödinger indipendente dal tempo:
$$\hat{H} u_n(x) = E_n u_n(x) \quad \text{con} \quad E_n = \hbar\omega \left(n + \frac{1}{2}\right)$$
Costituiscono una base ortonormale completa e comoda per diagonalizzare l'Hamiltoniana. Spesso a lezione vengono chiamati "gli stati standard dell'oscillatore", e questo genera la naturale confusione che siano "stati tipici o classici".

---

#### 3. Perché $u_n(x)$ è l'OPPOSTO di un oscillatore classico? (Il Paradosso di Schrödinger)

Dal punto di vista della fisica classica, gli stati $u_n(x)$ si comportano in modo **completamente anti-intuitivo e non-classico**:

| Proprietà | Oscillatore Armonico Classico (Molla/Pendolo) | Autostato Quantistico $u_n(x)$ (Stato di Fock $|n\rangle$) |
| :--- | :--- | :--- |
| **Movimento nel tempo** | Oscilla avanti e indietro: $x(t) = X_0 \cos(\omega t + \phi)$. | **È FERMO.** La densità di probabilità $\|\psi(x,t)\|^2 = \|u_n(x)\|^2$ è **statica, costante nel tempo**! |
| **Posizione media** | Varia periodicamente da $-X_0$ a $+X_0$. | $\langle x \rangle(t) = 0$ **sempre**, per qualsiasi $t$ e qualsiasi $n$. |
| **Impulso medio** | Varia da $-P_0$ a $+P_0$. | $\langle p \rangle(t) = 0$ **sempre**, per qualsiasi $t$. |
| **Fase dell'oscillazione** | Ben definita: $\phi = \omega t + \phi_0$. | **Completamente casuale**: $\Delta \phi = 2\pi$. |
| **Distribuzione spaziale** | Il punto materiale ha posizione esatta in ogni istante. | Ha $n$ **nodi** dove la probabilità è zero, e penetra nelle regioni classicamente proibite (effetto tunnel). |

> **Il paradosso:** Un pendolo o un'onda classica oscillano! Invece una particella preparata nell'autostato di Fock $u_n(x)$ ha valor medio nullo della posizione, valor medio nullo della velocità, e la sua nuvola di probabilità non si muove di un millimetro: **è un'onda stazionaria congelata**.  
> Non c'è nulla di classico in questo comportamento!

---

#### 4. Come nacquero allora gli Stati Coerenti? (Schrödinger, 1926)

Nel 1926, lo stesso **Erwin Schrödinger** rimase profondamente insoddisfatto da questo paradosso:  
*Come può la meccanica quantistica spiegare il moto di un pendolo classico macroscopico se tutti gli autostati $u_n(x)$ stanno fermi con $\langle x \rangle = 0$?*

Nel suo celebre articolo del 1926 (*"Der stetige Übergang von der Mikro- zur Makromechanik"*, ovvero *"Il passaggio continuo dalla micro- alla macro-meccanica"*), Schrödinger scoprì che per riottenere il comportamento di un oscillatore classico bisogna costruire una **sovrapposizione coerente di infiniti stati $u_n(x)$**:
$$|\alpha\rangle = e^{-|\alpha|^2/2} \sum_{n=0}^\infty \frac{\alpha^n}{\sqrt{n!}} |n\rangle$$
Sommando gli stati $u_n(x)$ con questi pesi specifici:
1. La nuvola di probabilità diventa un **pacchetto d'onda gaussiano compatto**.
2. Il pacchetto **oscilla avanti e indietro** seguendo esattamente la legge di Newton:
   $$\langle x \rangle(t) = x_0 \cos(\omega t), \quad \langle p \rangle(t) = -m\omega x_0 \sin(\omega t)$$
3. Il pacchetto **non si sparpaglia nel tempo** (non allarga la sua larghezza, a differenza di una particella libera).

Questi pacchetti d'onda scoperti da Schrödinger sono esattamente gli **stati coerenti $|\alpha\rangle$** formalizzati da Glauber negli anni '60 per descrivere la luce dei laser. Sono loro gli unici stati quantistici che si comportano classicamente!

---

#### 5. Riepilogo dei termini per non confondersi

* **"Autostati dell'energia / Stati stazionari"**: sono i ket $|n\rangle$, la cui funzione d'onda nello spazio delle coordinate è proprio la tua formula $u_n(x)$ con i polinomi di Hermite $H_n(x)$.
* **"Stati di Fock"**: è il nome che si usa in ottica quantistica e teoria dei campi per indicare gli stessi identici autostati dell'operatore numero $a^\dagger a|n\rangle = n|n\rangle$. Sono **stati puramente quantistici e non-classici** (varianza del numero di fotoni nulla $\Delta n = 0$, fase casuale, Wigner con $n$ anelli negativi).
* **"Stati classici dell'oscillatore"**: sono gli **stati coerenti $|\alpha\rangle$**, che combinano infiniti stati $u_n(x)$ per formare un pacchetto d'onda che oscilla nel tempo esattamente come un pendolo classico o un'onda elettromagnetica sinusoidale.

---

### Q&A #4 — Creare uno Stato di Fock eccitando i Qubit: cosa stiamo facendo davvero?

**Domanda:**  
*Quindi quando cerco di creare uno stato di Fock eccitando i qubit, sto cercando di generare un autostato dell'oscillatore armonico?*

---

#### 1. La Risposta Diretta: SÌ, esattamente!

Il nostro obiettivo finale è preparare la cavità elettromagnetica (che è a tutti gli effetti un oscillatore armonico quantistico) nell'autostato di Fock $|n\rangle$ (nel paper ad esempio $|n=6\rangle$).
Questo stato $|n\rangle$ è:
* L'autostato dell'operatore numero di fotoni: $a^\dagger a |n\rangle = n |n\rangle$.
* L'autostato dell'Hamiltoniana imperturbata della cavità:
  $$H_{\text{cav}} |n\rangle = \hbar\omega_c \left(n + \frac{1}{2}\right) |n\rangle$$

Vogliamo cioè che, una volta completato il protocollo al tempo finale $t=T$, **il campo elettromagnetico della cavità contenga esattamente $n$ fotoni**, senza alcuna fluttuazione nel numero ($\Delta n = 0$).

---

#### 2. Il Grande Problema: Perché non possiamo eccitare direttamente la cavità?

Perché abbiamo bisogno di passare attraverso i qubit e l'Effetto Casimir Dinamico? Perché non possiamo semplicemente "sparare" un'onda a microonde nella cavità alla frequenza di risonanza $\omega_c$ per portarla nello stato $|n=6\rangle$?

La risposta risiede nell'**equispaziatura dell'oscillatore armonico (la "trappola lineare")**:
1. In un oscillatore armonico, tutti i livelli energetici distano esattamente $\hbar\omega_c$:
   $$E_1 - E_0 = E_2 - E_1 = \dots = E_{n+1} - E_n = \hbar\omega_c$$
2. Se applichiamo un campo classico oscillante risonante direttamente alla cavità, l'operatore di interazione è lineare:
   $$H_{\text{drive\_cav}} \propto \mathcal{E}(t) (a + a^\dagger)$$
3. L'operatore di evoluzione generato da un drive lineare è l'operatore di spostamento di Glauber:
   $$D(\alpha) = \exp(\alpha a^\dagger - \alpha^* a)$$
   Applicato al vuoto $|0\rangle$, questo genera **SEMPRE E SOLO uno stato coerente $|\alpha\rangle$**:
   $$D(\alpha)|0\rangle = |\alpha\rangle = e^{-|\alpha|^2/2} \sum_{m=0}^\infty \frac{\alpha^m}{\sqrt{m!}} |m\rangle$$
4. In uno stato coerente, i fotoni sono distribuiti su **moltissimi livelli $m$ diversi** secondo una distribuzione di Poisson. È fisicamente **impossibile "fermarsi" al livello $|n=6\rangle$** pilotando solo l'oscillatore armonico in modo lineare!

> **La morale fondamentale:** Un oscillatore armonico puro non ha "selettività energetica". Se stimoli la transizione $0 \to 1$, stimoli contemporaneamente e con forza ancora maggiore le transizioni $1 \to 2$, $2 \to 3$, eccetera, arrampicandoti su una scala infinita!

---

#### 3. Il Ruolo Cruciale del Qubit: L'Anarmonicità e il Controllo

Per isolare e preparare un singolo livello $|n\rangle$, serve un elemento **fortemente non-lineare**: il **qubit**.
* Il qubit ha solo **due livelli** $\{|g\rangle, |e\rangle\}$: non è un oscillatore armonico infinito, ma un sistema saturo (una volta eccitato non può assorbire un secondo quanto alla stessa frequenza).
* Accoppiando il qubit alla cavità nel regime **USC** ($g/\omega_c \approx 0.3$), l'interazione $g(a+a^\dagger)\sigma_x$ "ibridizza" i livelli della cavità e del qubit, creando autostati congiunti fortemente anarmonici.

---

#### 4. Cosa succede DURANTE e ALLA FINE del protocollo?

La dinamica del tuo stage si divide in due regimi temporali concettualmente diversi:

```
t = 0 (Inizio)               0 < t < T (Dinamica di Controllo)               t = T (Fine)
────────────────────────────────────────────────────────────────────────────────────────────
Vuoto congiunto:             Stato quantistico complesso ed entangled:      Stato target desiderato:
|ψ(0)⟩ = |0, g, g⟩          |ψ(t)⟩ = Σ c_{m,s1,s2}(t) |m⟩_cav |s1, s2⟩_q    |ψ(T)⟩ ≈ |n⟩_cav ⊗ |g, g⟩
                                                                            
• 0 fotoni                   • I qubit vengono modulati da Ω_D(t)           • Il drive si spegne
• Qubit in |g, g⟩            • Termini contro-rotanti a† σ+ creano         • I qubit tornano in |g, g⟩
• Parità +1                    coppie di eccitazioni dal vuoto (DCE)        • Cavità "congelata" in |n⟩
                             • Forte entanglement tra cavità e qubit        • Fedeltà F ≈ 0.995
```

1. **Durante il processo ($0 < t < T$):**
   * Il sistema **NON** si trova affatto in un autostato della cavità!
   * Modulando la frequenza del qubit $\Omega_D(t)$ a velocità non-adiabatica, i termini contro-rotanti estraggono coppie di eccitazioni dal vuoto quantistico tramite l'Effetto Casimir Dinamico.
   * La cavità e i qubit sono fortemente entangled in uno spazio a 120 dimensioni (per 2 qubit).
2. **Al tempo finale ($t = T$):**
   * Gli algoritmi di controllo ottimo (CRAB + GRAPE) hanno calcolato la forma di $\Omega_D(t)$ proprio affinché a $t=T$ si verifichi un'**interferenza distruttiva per tutte le componenti indesiderate** e un'**interferenza costruttiva solo per lo stato $|n\rangle$**.
   * Il drive si spegne dolcemente ($\Omega_D(T) \to 0$).
   * I qubit si disaccoppiano e tornano nel fondamentale $|g, g\rangle$.
   * La cavità resta "intrappolata" con fedeltà quasi unitaria ($F \approx 0.995$) esattamente nell'autostato di Fock $|n\rangle$ dell'oscillatore armonico!

---

#### 5. Il nesso con il tuo progetto a 2 Qubit

Nel caso a 1 qubit del paper, un solo qubit deve "farsi carico" di tutta l'anarmonicità e di tutta l'energia di modulazione $\Omega_D(t)$ necessaria per creare $n$ fotoni (ad esempio $n=6$).  
**Nel tuo stage con 2 qubit:**
* Abbiamo **due attuatori quantistici indipendenti** ($\Omega_{D1}(t)$ e $\Omega_{D2}(t)$) accoppiati alla stessa cavità.
* Possono cooperare per "scolpire" l'autostato $|n\rangle$ dell'oscillatore armonico con ampiezze di pilotaggio più basse, minor energia $C^2$ e minore stress sperimentale sui singoli qubit!

---

### Q&A #5 — L'Effetto Casimir Dinamico (DCE): è programmato nel codice o emerge dalla fisica?

**Domanda:**  
*L'effetto DCE (Dynamical Casimir Effect) come è stato incorporato nella libreria / nel codice? È stato programmato esplicitamente dentro con qualche funzione apposita, o esce spontaneamente dalla modellizzazione della realtà?*

---

#### 1. La Risposta: Emerge al 100% Spontaneamente dalla Fisica!

**Non c'è nessuna riga di codice che menzioni il DCE, né alcuna funzione o comando che dica al computer di "creare fotoni".**

Il computer non sa assolutamente cosa sia l'Effetto Casimir Dinamico. Tutto ciò che fa il software (e la libreria QuTiP) è eseguire pura e semplice **algebra lineare**:
1. Definisce delle matrici costanti per gli operatori:
   * $a = \text{destroy(dim)}$ $\to$ una matrice numerica $30 \times 30$ con $\sqrt{n}$ sulla sotto-diagonale.
   * $\sigma_x = \text{sigmax()}$, $\sigma_z = \text{sigmaz()}$ $\to$ matrici $2 \times 2$.
2. Assembla l'Hamiltoniana totale $H(t)$ tramite prodotti tensoriali:
   $$H(t) = \omega_c a^\dagger a + g(a + a^\dagger)\sigma_x + \frac{\Omega_D(t)}{2}\sigma_z$$
3. Risolve numericamente l'equazione di Schrödinger dipendente dal tempo (`sesolve` o $U = e^{-i H(t) \Delta t}$):
   $$i \hbar \frac{d}{dt} |\psi(t)\rangle = H(t) |\psi(t)\rangle \implies |\psi(t + \Delta t)\rangle \approx \exp\left(-\frac{i}{\hbar} H(t) \Delta t\right) |\psi(t)\rangle$$

Il solutore fa solo una cosa meccanica: calcola l'esponenziale di una matrice (di dimensione $120 \times 120$ nel caso a due qubit) e la moltiplica per un vettore di numeri complessi che parte da $|0, g, g\rangle = (1, 0, 0, \dots, 0)^T$.

Eppure, a fine simulazione, **il numero medio di fotoni $\langle a^\dagger a \rangle(t)$ cresce da $0$ a $6$ fotoni reali!**

---

#### 2. Da DOVE esce allora il DCE? (L'anatomia matematica dell'effetto)

Il DCE emerge in modo naturale e ineluttabile dall'incontro tra **due soli ingredienti matematici** scritti nell'Hamiltoniana:

##### Ingrediente 1: I termini contro-rotanti $a^\dagger \sigma_+$
Quando scriviamo l'interazione luce-materia fisica:
$$g(a + a^\dagger)\sigma_x = g (a + a^\dagger)(\sigma_+ + \sigma_-) = g(a\sigma_+ + a^\dagger\sigma_- + \underbrace{a^\dagger\sigma_+}_{\text{creazione di coppie}} + a\sigma_-)$$
il termine $a^\dagger\sigma_+$ ha un elemento di matrice **non nullo** tra lo stato di vuoto $|0, g\rangle$ e lo stato eccitato $|1, e\rangle$:
$$\langle 1, e | a^\dagger\sigma_+ |0, g\rangle = 1 \neq 0$$
Nella matrice dell'Hamiltoniana $H$, questo significa che ci sono numeri diversi da zero fuori dalla diagonale che collegano direttamente il "blocco a zero fotoni" al "blocco a fotoni ed eccitazioni non nulle".

##### Ingrediente 2: La dipendenza temporale non-adiabatica $\Omega_D(t)$
* Se il sistema fosse stazionario ($\Omega_D = \text{costante}$), per conservazione dell'energia il sistema rimarrebbe nel suo stato fondamentale (che nel regime USC contiene solo fotoni virtuali vestiti, ma nessun fotone reale osservabile).
* Ma quando applichiamo il drive esterno $\Omega_D(t)$, l'Hamiltoniana **dipende dal tempo**:
  $$\frac{dH}{dt} \neq 0$$
  In meccanica quantistica, un'Hamiltoniana dipendente dal tempo **non conserva l'energia del sistema**: il generatore esterno compie lavoro termodinamico sul sistema quantistico.

##### Il risultato: la conversione di fluttuazioni in particelle reali
La modulazione rapida $\Omega_D(t)$ (a frequenze vicine alla risonanza parametrica $\approx 2\omega_c$) fornisce esattamente i quanti di energia necessari per soddisfare la condizione di risonanza dei termini contro-rotanti.  
Il generatore unitario $U(t) = \mathcal{T}\exp\left(-i \int_0^t H(t') dt'\right)$ mescola inevitabilmente gli operatori di annichilazione e creazione:
$$a(t) = U^\dagger(t) a U(t) = u(t) a + v(t) a^\dagger \quad (\text{Trasformazione di Bogoliubov})$$
Poiché $v(t) \neq 0$, il valore di aspettazione del numero di fotoni sul vuoto iniziale diventa:
$$\langle 0 | a^\dagger(t) a(t) | 0 \rangle = |v(t)|^2 > 0$$
I fotoni vengono materializzati dal vuoto. **Questa formula è esattamente la definizione teorica dell'Effetto Casimir Dinamico!**

---

#### 3. La controprova: Cosa succederebbe se usassimo il modello di Jaynes-Cummings?

Immagina di modificare una sola riga di codice in `two_qubit_system.py`: invece di mettere l'accoppiamento di Rabi completo $g(a+a^\dagger)\sigma_x$, decidiamo di eliminare a mano i termini contro-rotanti (usando Jaynes-Cummings):
$$H_{\text{int\_JC}} = g(a \sigma_+ + a^\dagger \sigma_-)$$
Cosa farebbe il solutore numerico `sesolve` se facessimo girare l'ottimizzazione?
1. Applicando $H_{\text{int\_JC}}$ sullo stato iniziale $|0, g\rangle$:
   $$a \sigma_+ |0, g\rangle = 0 \quad (\text{perché } a|0\rangle = 0)$$
   $$a^\dagger \sigma_- |0, g\rangle = 0 \quad (\text{perché } \sigma_-|g\rangle = 0)$$
2. Applicando il drive $H_D(t) = \frac{\Omega_D(t)}{2}\sigma_z$:
   $$\sigma_z |0, g\rangle = -|0, g\rangle \quad (\text{cambia solo una fase globale!})$$
3. Il vettore di stato rimarrebbe **inchiodato per sempre nel vuoto**:
   $$|\psi(t)\rangle = e^{i \phi(t)} |0, g\rangle \implies \langle n \rangle(t) = 0 \quad \forall t$$
Anche fornendo una potenza infinita a $\Omega_D(t)$, **non si creerebbe nemmeno un singolo fotone! L'effetto DCE svanirebbe istantaneamente.**

---

#### 4. La bellezza della fisica computazionale

Questo evidenzia uno dei principi più profondi della fisica moderna:  
Non serve programmare ad hoc i singoli fenomeni fisici (come il DCE, la decoerenza, o l'interferenza). Basta programmare le **leggi fondamentali corrette** (l'equazione di Schrödinger e l'Hamiltoniana con tutte le sue interazioni fisiche non approssimate).  
Tutti i fenomeni complessi della natura emergono da soli come conseguenza matematica inevitabile di quelle leggi!

---

### Q&A #6 — Cosa Significa che "È Conservata la Parità"? Regole di Selezione e Creazione a Coppie

**Domanda:**  
*Nel paper si legge che l'Hamiltoniana di Rabi e l'Hamiltoniana di controllo conservano la parità $\Pi = e^{i\pi n_{\text{ex}}}$. Cosa significa fisicamente e matematicamente che la parità è conservata? Quali conseguenze pratiche ha sulle simulazioni?*

---

#### 1. Definizione dell'Operatore di Parità

Nel nostro sistema congiunto (Cavità + Qubit), il **numero totale di eccitazioni** è dato da:
$$n_{\text{ex}} = a^\dagger a + \sigma_+ \sigma_-$$
* $a^\dagger a$ conta il numero di fotoni nella cavità ($0, 1, 2, 3, \dots$).
* $\sigma_+ \sigma_- = |e\rangle\langle e|$ vale $0$ se il qubit è nello stato fondamentale $|g\rangle$ e $1$ se è nello stato eccitato $|e\rangle$.

L'**operatore di parità** $\Pi$ misura se il numero totale di eccitazioni è **pari** o **dispari**:
$$\Pi := e^{i\pi n_{\text{ex}}} = (-1)^{n_{\text{ex}}} = -\sigma_z e^{i\pi a^\dagger a}$$

Questo operatore ha solo due possibili autovalori:
* **$+1$ (Parità Pari / Even):** se $n_{\text{ex}}$ è pari ($0, 2, 4, 6, \dots$).
  * Esempi: $|0, g\rangle$ (0 eccitazioni), $|2, g\rangle$ (2 eccitazioni), $|1, e\rangle$ (2 eccitazioni), $|6, g\rangle$ (6 eccitazioni).
* **$-1$ (Parità Dispari / Odd):** se $n_{\text{ex}}$ è dispari ($1, 3, 5, 7, \dots$).
  * Esempi: $|1, g\rangle$ (1 eccitazione), $|0, e\rangle$ (1 eccitazione), $|3, g\rangle$ (3 eccitazioni), $|2, e\rangle$ (3 eccitazioni).

---

#### 2. Il Significato Matematico: La Simmetria $[\Pi, H(t)] = 0$

Dire che la parità è una **costante del moto** (o quantità conservata) significa che l'operatore $\Pi$ **commuta con l'Hamiltoniana totale a qualsiasi istante di tempo $t$**:
$$[\Pi, H_S(t)] = \Pi H_S(t) - H_S(t) \Pi = 0 \quad \forall t$$

Dall'equazione del moto di Heisenberg (o teorema di Ehrenfest):
$$\frac{d}{dt} \langle \Pi \rangle = \frac{i}{\hbar} \langle [H_S(t), \Pi] \rangle = 0 \implies \langle \Pi \rangle(t) = \text{costante}$$

##### Perché $[\Pi, H] = 0$?
L'operatore di parità inverte il segno degli operatori di creazione/annichilazione e di salto del qubit:
$$\Pi a \Pi^\dagger = -a, \quad \Pi a^\dagger \Pi^\dagger = -a^\dagger, \quad \Pi \sigma_\pm \Pi^\dagger = -\sigma_\pm, \quad \Pi \sigma_z \Pi^\dagger = +\sigma_z$$
Guardiamo i singoli pezzi dell'Hamiltoniana:
* La cavità libera $a^\dagger a \to (-a^\dagger)(-a) = +a^\dagger a$ (invariante).
* Il qubit libero e il controllo $\sigma_z \to +\sigma_z$ (invariante).
* L'interazione di Rabi $(a + a^\dagger)(\sigma_+ + \sigma_-) \to [-(a + a^\dagger)][-(\sigma_+ + \sigma_-)] = +(a + a^\dagger)(\sigma_+ + \sigma_-)$ (invariante!).

I due segni meno si moltiplicano dando un segno **più**! L'Hamiltoniana è invariante per riflessione di parità.

---

#### 3. Lo Spazio di Hilbert si Spezza in Due Mondi Disgiunti

Poiché $[\Pi, H(t)] = 0$, l'intero spazio di Hilbert del sistema (di dimensione $30 \times 2 = 60$ a un qubit, o $120$ a due qubit) si suddivide in due sottospazi ortogonali e non comunicanti:
$$\mathcal{H} = \mathcal{H}_{\text{pari}} \oplus \mathcal{H}_{\text{dispari}}$$
Nessun termine dell'Hamiltoniana ha elementi di matrice tra i due mondi:
$$\langle \psi_{\text{dispari}} | H(t) | \phi_{\text{pari}} \rangle = 0$$

L'evoluzione quantistica **non può saltare da un sottospazio all'altro**:
$$\text{Se parti da uno stato PARI} \implies \text{rimani in uno stato PARI per l'eternità!}$$

---

#### 4. La Conseguenza Fisica Fondamentale: Le Eccitazioni nascono A COPPIE

Nel nostro esperimento partiamo dal vuoto assoluto:
$$|\psi(0)\rangle = |0\rangle_{\text{cav}} |g\rangle_{\text{qubit}}$$
* Fotoni: $0$
* Eccitazioni del qubit: $0$
* Parità iniziale: $\Pi |0, g\rangle = (-1)^0 |0, g\rangle = \mathbf{+1}$ **(PARI)**.

Poiché la parità si conserva, per qualsiasi tempo $t > 0$, **la parità totale deve rimanere $+1$**.
Vediamo cosa possono fare i singoli operatori:

```
Termine dell'Hamiltoniana     Cosa fa allo stato                         Variazione Δn_ex
────────────────────────────────────────────────────────────────────────────────────────
a† σ-                         Crea 1 fotone, diseccita il qubit         +1 - 1 =  0  (pari)
a σ+                          Distrugge 1 fotone, eccita il qubit       -1 + 1 =  0  (pari)
a† σ+ (Contro-rotante)        Crea 1 fotone ED eccita il qubit          +1 + 1 = +2  (pari!)
a σ-  (Contro-rotante)        Distrugge 1 fotone E diseccita il qubit   -1 - 1 = -2  (pari!)
Ω_D(t) σz (Controllo)         Modula la fase, non cambia eccitazioni    0            (pari)
```

In qualsiasi transizione quantistica elementare, la variazione del numero di eccitazioni $\Delta n_{\text{ex}}$ è **$0$, $+2$ o $-2$**. Non può **MAI essere $\pm 1$**!  
**I fotoni e le eccitazioni possono essere creati o distrutti ESCLUSIVAMENTE A COPPIE.**

---

#### 5. Regole di Selezione: Cosa si può creare e cosa è IMPOSSIBILE?

A fine protocollo ($t = T$), vogliamo che il drive si spenga e che il qubit ritorni nel suo stato fondamentale $|g\rangle$ (0 eccitazioni del qubit).
Dalla legge di conservazione:
$$\Pi_{\text{totale}} = \Pi_{\text{cav}} \times \Pi_{\text{qubit}} = (-1)^{n_{\text{cav}}} \times (-1)^0 = (-1)^{n_{\text{cav}}} \equiv +1$$
Ne consegue inevitabilmente che:
$$n_{\text{cav}} \text{ deve essere un numero PARI!}$$

##### A. Stati permessi (accessibili dal vuoto $|0, g\rangle$):
* **Stati di Fock PARI:** $|n = 2\rangle, |n = 4\rangle, |n = 6\rangle, |n = 8\rangle, \dots$  
  *(Ecco svelato il motivo per cui il paper sceglie come benchmark $|n=6\rangle$ e non $|n=5\rangle$ o $|n=7\rangle$!)*
* **Stati Squeezed:** contengono solo componenti con numero pari di fotoni ($|0\rangle, |2\rangle, |4\rangle\dots$).
* **Even Cat States:** $C_\alpha^+ \propto |\alpha\rangle + |-\alpha\rangle$ (hanno solo fotoni pari).

##### B. Stati SEVERAMENTE PROIBITI dal vuoto $|0, g\rangle$:
* **Stati di Fock DISPARI:** $|n = 1\rangle, |n = 3\rangle, |n = 5\rangle, \dots$
* Se provassi a far girare il tuo script `run_crab_2q.py` o `run_grape_2q.py` impostando `n_target = 1` o `n_target = 5` partendo da $|0, g, g\rangle$:
  **L'algoritmo darebbe FEDELTÀ ZERO (o trascurabile numericamente)!**  
  Non perché l'ottimizzatore non è bravo, ma perché la conservazione della parità impone $\langle 1, g, g | \psi(t) \rangle \equiv 0$ a livello di legge di conservazione fondamentale!

##### Come si creerebbero gli stati dispari?
Se un domani volessi creare uno stato con un numero dispari di fotoni (es. $|n=1\rangle$), dovresti:
1. Partire da uno stato iniziale con parità dispari, ad esempio preparando prima il qubit nello stato eccitato $|0, e\rangle$ ($\Pi = -1$); oppure
2. Aggiungere nell'Hamiltoniana un termine che **rompe la simmetria di parità** (ad esempio un drive sul qubit proporzionale a $\sigma_x$, che non commuta con $\Pi$).

---

#### 6. Il Caso del tuo Stage: Conservazione della Parità a 2 Qubit

Nel tuo sistema cavità + 2 qubit, l'operatore di parità diventa:
$$\Pi = \exp[i\pi (a^\dagger a + \sigma_{+1}\sigma_{-1} + \sigma_{+2}\sigma_{-2})]$$
Lo stato iniziale è $|0, g, g\rangle$, che ha ancora $n_{\text{ex}} = 0$ e parità **$+1$ (PARI)**.
* Se entrambi i qubit tornano in $|g, g\rangle$, la cavità deve avere un numero **pari** di fotoni ($|n=2, 4, 6\dots\rangle$).
* Ma a 2 qubit c'è una ricchezza in più: se i qubit finiscono in uno stato di Bell entangled con parità pari come $|\Phi^+\rangle = \frac{|gg\rangle + |ee\rangle}{\sqrt{2}}$, la parità è ancora rispettata e si possono generare stati entangled qubit-qubit direttamente dal vuoto!





