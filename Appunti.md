## 1
Chiedere se e che tipo di interazione si avrebbe tr i due qubit direttamente, nel caso aggiungere all'hamiltoniana di drift: 

Accoppiamento diretto qubit-qubit (es. tipo XX+YY)
sy1 = tensor(I_c, sigmay(), I_q)
sy2 = tensor(I_c, I_q, sigmay())
H_qq = J_direct * (sx1 * sx2 + sy1 * sy2)

H0 = omega_c * (n_tot + 0.5 * identity) + g1 * x_couple1 + g2 * x_couple2 + H_qq

## 2

