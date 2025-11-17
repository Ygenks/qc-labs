from gates import iter_gate

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from matplotlib import pyplot as plt

N = 3
N_CLBITS = N

qreg_a = QuantumRegister(N, 'a')
qreg_b = QuantumRegister(N, 'b')
qreg_overflow = QuantumRegister(1, 'o')

clreg = ClassicalRegister(N)
clreg_overflow = ClassicalRegister(1)

qc = QuantumCircuit(qreg_a, qreg_b, qreg_overflow, clreg, clreg_overflow)

qc.x(qreg_a)
qc.x(qreg_b[2])

iter_g = iter_gate(qc.find_bit(qreg_a[0]).index, qreg_a.size, qc.find_bit(qreg_b[0]).index, qreg_b.size, qc.find_bit(qreg_overflow[0]).index)

qc.append(iter_g, qc.qubits)

qc.measure(qreg_a, clreg)
qc.measure(qreg_overflow, clreg_overflow)

simulator = AerSimulator()

qc_transpiled = transpile(qc, simulator)
result = simulator.run(qc_transpiled).result()

statistics = result.get_counts()

for outcome, frequency in statistics.items():
    print(f'Measured {outcome} with frequency {frequency}')

qc.draw(output='mpl')
plt.show()
