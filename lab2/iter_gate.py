import itertools
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from gates import subo_gate, cadd_gate

from qiskit import QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

from matplotlib import pyplot as plt


my_style = {
    'displaycolor': {
        'iter': [  # gate name
            '#FFE4E1',  # box color
            '#000000',  # box text color
        ],
        'div': [  # gate name
            '#FFE4E1',  # box color
            '#000000',  # box text color
        ],
        'mult': [  # gate name
            '#FFE4E1',  # box color
            '#000000',  # box text color
        ],
        'addo': [
            '#FFE4E1',  # box color
            '#000000',  # box text color
        ],
        'subo': [
            '#FFE4E1',  # box color
            '#000000',  # box text color
        ],
        'cadd': [
            '#FFE4E1',  # box color
            '#000000',  # box text color
        ],
    }
}


class IterGate(Gate):
    def __init__(self, a_start, a_size, b_start, b_size, overflow):
        # 2n for quantum registers and 1 classical overflow bit
        self.n = a_size + b_size + 1

        super().__init__('iter', self.n, [])

        self.a_start = a_start
        self.a_size = a_size
        self.b_start = b_start
        self.b_size = b_size
        self.overflow = overflow

        self._define()

    def _define(self):
        qc = QuantumCircuit(self.n, name='iter')

        subo = subo_gate(self.a_start, self.a_size, self.b_start, self.b_size, self.overflow)
        cadd = cadd_gate(self.a_start, self.a_size, self.b_start, self.b_size, self.overflow)

        qc.append(subo, qc.qubits)
        qc.append(cadd, qc.qubits)

        qc.x(self.overflow)

        self.definition = qc

        # qc.draw(filename='iter_gate', output='mpl',scale=0.4,style=my_style)


if __name__ == '__main__':
    # n = 3

    # # Build circuit
    # qreg_a = QuantumRegister(n, 'a')
    # qreg_b = QuantumRegister(n, 'b')
    # qreg_o = QuantumRegister(1, 'o')

    # clreg_res = ClassicalRegister(n)
    # clreg_o = ClassicalRegister(1)

    # qc = QuantumCircuit(qreg_a, qreg_b, qreg_o, clreg_res, clreg_o)

    # iter_gate = IterGate(0, n, n, n, 2 * n)
    # qc.append(iter_gate, qc.qubits)

    # # Measure
    # qc.measure(qreg_a, clreg_res)
    # qc.measure(qreg_o, clreg_o)

    # sim = AerSimulator()
    # compiled = transpile(qc, sim)
    # result = sim.run(compiled).result()
    # counts = result.get_counts()

    # print(counts)

    n = 3
    m = 2

    # Build circuit
    qreg_data = QuantumRegister(n + m + n + m + 1, 'd')
    clreg_quotient = ClassicalRegister(n + m)
    clreg_remainder = ClassicalRegister(n)

    qc = QuantumCircuit(qreg_data, clreg_quotient, clreg_remainder)

    qc.x(0)
    qc.x(2)
    qc.x(3)
    qc.x(4)

    qc.x(qc.qubits[-n:])

    i = n + m - 1
    while i >= 0:
        # iter_gate = IterGate(i, n, i + n + 1, n, i + n)
        iter_gate = IterGate(0, n, n + 1, n, n)

        target_a = list(qc.qubits[i: i + n])
        target_o = [qc.qubits[i + n]]
        target_b = list(qc.qubits[-n:])

        target_qubits = target_a + target_o + target_b

        qc.append(iter_gate, target_qubits)

        i -= 1

    qc.barrier()

    qc.measure(range(0, n), clreg_remainder)

    qc.measure(range(n, 2 * n + m), clreg_quotient)

    qc.draw(output='mpl')
    plt.show()

    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()

    print(counts)
