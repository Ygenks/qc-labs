from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from gates import subo_gate, cadd_gate

from qiskit import QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

my_style = {
    "displaycolor": {
        "iter": [ # gate name
            "#FFE4E1", # box color
            "#000000"  # box text color
        ],
        "div": [ # gate name
            "#FFE4E1", # box color
            "#000000"  # box text color
        ],
        "mult": [ # gate name
            "#FFE4E1", # box color
            "#000000"  # box text color
        ],
        "addo": [
            "#FFE4E1", # box color
            "#000000"  # box text color
        ],
        "subo": [
            "#FFE4E1", # box color
            "#000000"  # box text color
        ],
        "cadd": [
            "#FFE4E1", # box color
            "#000000"  # box text color
        ]
}}


class IterGate(Gate):
    def __init__(self, n):
        # 2n for quantum registers and 1 classical overflow bit
        super().__init__('iter', 2 * n + 1, [])
        self.n = n

        self._define()

    def _define(self):
        n = self.n

        qc = QuantumCircuit(2 * n + 1, name='iter')

        subo = subo_gate(0, n, n, n, 2 * n)
        cadd = cadd_gate(0, n, n, n, 2 * n)

        qc.append(subo, qc.qubits)
        qc.append(cadd, qc.qubits)

        qc.x(qc.qubits[-1])

        self.definition = qc

        # qc.draw(filename='iter_gate', output='mpl',scale=0.4,style=my_style)


if __name__ == '__main__':

    n = 3

    # Build circuit
    qreg_a = QuantumRegister(n, 'a')
    qreg_b = QuantumRegister(n, 'b')
    qreg_o = QuantumRegister(1, 'o')

    clreg_res = ClassicalRegister(n)
    clreg_o = ClassicalRegister(1)

    qc = QuantumCircuit(qreg_a, qreg_b, qreg_o, clreg_res, clreg_o)

    iter_gate = IterGate(n)
    qc.append(iter_gate, qc.qubits)

    # Measure
    qc.measure(qreg_a, clreg_res)
    qc.measure(qreg_o, clreg_o)

    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()

    print(counts)

