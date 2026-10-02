# Report Simulazione Quantum Optimal Control — 2Q

**Data e Ora Esecuzione:** 2026-10-02 12:17:00  
**Cartella:** `run_2026-10-02_12-17-00`  

## 1. Risultati Chiave
| Fase | Fedeltà ($\mathcal{F}$) | Costo Energetico ($C^2$) | Tempo Esecuzione | Iterazioni / Note |
| :--- | :---: | :---: | :---: | :--- |
| **CRAB (Miglior Seed #2)** | `0.979144` | `1383.58` | `0.0s` | Media 0.9693 ± 0.0072 |
| **GRAPE (L-BFGS-B)** | `0.999906` | `987.73` | `0.0s` | 500 iterazioni |
| **PCHIP Smoothed (Finale)** | **`0.987673`** | **`981.63`** | `0.0s` | Interpolazione fine (600 pts) |

## 2. Metriche Fisiche dell'Attuatore
| Canale | Slew Rate Max $\max|d\Omega/dt|$ | Slew Rate RMS | Costo Canale $C_k^2$ | Banda 99% $\omega_{99\%}$ |
| :--- | :---: | :---: | :---: | :---: |
| Qubit 1 | `8.007` | `1.682` | `520.93` | `5.81` $\omega_c$ |
| Qubit 2 | `8.396` | `1.813` | `460.70` | `5.99` $\omega_c$ |

## 3. Parametri di Configurazione
- **Stato Target:** Fock |n=10⟩ (Fotoni attesi $\langle n \rangle = 10.00$)
- **Dimensione Spazio Fock:** 40 (Dimensione totale: 160)
- **Durata Evoluzione $T$:** 104.720 ($T/\tau_s = 20.00$, $\tau_s = 5.236$)
- **CRAB:** 10 seeds paralleli, 20 armoniche, taglio $\omega \in [0, 3.0\omega_c]$, $N_t = 400$
- **GRAPE:** $N_t = 300$ time slots (taglio Nyquist $\omega_{\text{Nyq}} = 8.97\omega_c$), bound ampiezza (0.5, 3.0)
- **Tempo totale simulazione:** 0.0s (0.00 min)

## 4. Grafici Analitici Generati
1. **Numero medio di fotoni:** [nmean.pdf](nmean.pdf)  
   ![Numero medio fotoni](nmean.png)

2. **Confronto Forme d'Onda di Controllo:** [drives_comparison.pdf](drives_comparison.pdf)  
   ![Controlli](drives_comparison.png)

3. **Funzioni di Wigner (Target vs Finale):** [wigner.pdf](wigner.pdf)  
   ![Wigner](wigner.png)

4. **Spettro di Fourier (FFT):** [fft.pdf](fft.pdf)  
   ![FFT](fft.png)
