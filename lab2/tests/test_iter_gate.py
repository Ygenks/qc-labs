import pytest
from itertools import product

from qiskit_aer import AerSimulator
from qiskit import transpile

from divider import build_iter_circuit

def build_iter_circuit(reg_a_size, reg_b_size):

    qreg_a = QuantumRegister(, 'a')
    qreg_b = QuantumRegister(, 'b')
    qreg_overflow = QuantumRegister(1, 'o')

    clreg = ClassicalRegister(N)
    clreg_overflow = ClassicalRegister(1)

    circuit = QuantumCircuit(qreg_a, qreg_b, qreg_overflow, clreg, clreg_overflow)

    circuit.x(qreg_a)
    circuit.x(qreg_b[2])

    iter_g = iter_gate(circuit.find_bit(qreg_a[0]).index, qreg_a.size, circuit.find_bit(qreg_b[0]).index, qreg_b.size, circuit.find_bit(qreg_overflow[0]).index)

    circuit.append(iter_g, circuit.qubits)


    return circuit



def generate_all_inputs():
    bits = list(product([0, 1], repeat=3))
    for a in bits:
        for b in bits:
            yield a, b


@pytest.mark.parametrize("init_a, init_b", generate_all_inputs())
def test_iter_gate_all_inputs(init_a, init_b):


    qc = build_iter_circuit(init_a, init_b)

    qc.measure(qreg_a, clreg)
    qc.measure(qreg_overflow, clreg_overflow)

    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()

    assert isinstance(counts, dict)
    assert len(counts) > 0

    print(f"A={init_a}, B={init_b} → counts={counts}")

    # If you later know expected behavior:
    # expected = {...}
    # assert counts == expected
