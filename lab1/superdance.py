from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from matplotlib import pyplot as plt

qc = QuantumCircuit(4, 4)

qc.h(0)
qc.h(2)

qc.cx(0, 1)
qc.cx(2, 3)

qc.barrier()

qc.x(0)
qc.z(2)

qc.barrier()

qc.cx(0, 1)
qc.cx(2, 3)

qc.h(0)
qc.h(2)

# qc.measure([0, 1, 2, 3], [1, 0, 3, 2])
# qc.measure([2,3],[2, 3])
qc.measure_all(add_bits=False)

result = AerSimulator().run(qc).result()
statistics = result.get_counts()

for outcome, frequency in statistics.items():
    print(f'Measured {outcome} with frequency {frequency}')

qc.draw(output='mpl')
plt.show()
