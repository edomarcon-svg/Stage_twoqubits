# Report Simulazione Quantum Optimal Control — 1Q

**Data e Ora Esecuzione:** 2026-10-02 17:11:51  
**Cartella:** `1q`  

## 1. Risultati Chiave
| Fase | Fedeltà ($\mathcal{F}$) | Costo Energetico ($C^2$) | Tempo Esecuzione | Iterazioni / Note |
| :--- | :---: | :---: | :---: | :--- |
| **CRAB (Miglior Seed #5)** | `0.969828` | `497.23` | `448.2s` | Media 0.9097 ± 0.0579 |
| **GRAPE (L-BFGS-B)** | `0.872035` | `227.65` | `660.1s` | 150 iterazioni |
| **PCHIP Smoothed (Finale)** | **`0.839708`** | **`220.20`** | `2.6s` | Interpolazione fine (600 pts) |

## 2. Metriche Fisiche dell'Attuatore
| Canale | Slew Rate Max $\max|d\Omega/dt|$ | Slew Rate RMS | Costo Canale $C_k^2$ | Banda 99% $\omega_{99\%}$ |
| :--- | :---: | :---: | :---: | :---: |
| Qubit 1 | `10.450` | `3.293` | `220.20` | `9.94` $\omega_c$ |

## 3. Parametri di Configurazione
- **Stato Target:** Fock |n=10⟩ (Fotoni attesi $\langle n \rangle = 10.00$)
- **Dimensione Spazio Fock:** 40 (Dimensione totale: 80)
- **Durata Evoluzione $T$:** 52.360 ($T/\tau_s = 10.00$, $\tau_s = 5.236$)
- **CRAB:** 6 seeds paralleli, 20 armoniche, taglio $\omega \in [0, 3.0\omega_c]$, $N_t = 400$
- **GRAPE:** $N_t = 150$ time slots (taglio Nyquist $\omega_{\text{Nyq}} = 8.94\omega_c$), bound ampiezza (0.5, 3.0)
- **Tempo totale simulazione:** 1113.4s (18.56 min)

## 4. Grafici Analitici Generati
1. **Numero medio di fotoni:** [nmean.pdf](nmean.pdf)  
   ![Numero medio fotoni](nmean.png)

2. **Confronto Forme d'Onda di Controllo:** [drives_comparison.pdf](drives_comparison.pdf)  
   ![Controlli](drives_comparison.png)

3. **Funzioni di Wigner (Target vs Finale):** [wigner.pdf](wigner.pdf)  
   ![Wigner](wigner.png)

4. **Spettro di Fourier (FFT):** [fft.pdf](fft.pdf)  
   ![FFT](fft.png)
