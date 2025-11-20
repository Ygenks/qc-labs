import pytest
from itertools import product

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile

from iter_gate import IterGate

N = 3


def generate_input(n):
    bits = list(product([0, 1], repeat=n))
    for a in bits:
        for b in bits:
            yield a, b


@pytest.mark.parametrize('init_a, init_b', generate_input(N))
def test_iter_gate_n2(init_a, init_b):
    n = N

    # Build circuit
    qreg_a = QuantumRegister(n, 'a')
    qreg_b = QuantumRegister(n, 'b')
    qreg_o = QuantumRegister(1, 'o')

    clreg_res = ClassicalRegister(n)
    clreg_o = ClassicalRegister(1)

    qc = QuantumCircuit(qreg_a, qreg_b, qreg_o, clreg_res, clreg_o)

    for i in range(n):
        if init_a[i] == 1:
            qc.x(qreg_a[i])
        if init_b[i] == 1:
            qc.x(qreg_b[i])

    iter_gate = IterGate(0, n, n, n, 2 * n)
    qc.append(iter_gate, qc.qubits)

    qc.measure(qreg_a, clreg_res)
    qc.measure(qreg_o, clreg_o)

    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()

    outcome = list(counts.keys())[0]

    measured_o = int(outcome[0])
    measured_a = int(outcome[1:], 2)

    a_binary = ''.join(str(b) for b in reversed(init_a))
    a_int = int(a_binary, 2)

    b_binary = ''.join(str(b) for b in reversed(init_b))
    b_int = int(b_binary, 2)

    if a_int >= b_int:
        expected_o = 1
        expected_a = a_int - b_int
    else:
        expected_o = 0
        expected_a = a_int

    assert measured_o == expected_o
    assert measured_a == expected_a, f'Outcome: {outcome}, init_a:{init_a}, init_b:{init_b}'
