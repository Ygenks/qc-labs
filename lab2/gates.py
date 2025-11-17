from qiskit.circuit import QuantumCircuit, QuantumRegister

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

def addo_gate(qAStart, qASize, qBStart, qBSize, o, draw=False):

    if qASize != qBSize:
        raise ValueError("size of Reg A not equal to size of Reg B")

    n      = qASize
    nQBits = qASize+qBSize+1
    circ   = QuantumCircuit(QuantumRegister(nQBits,'d'))

    for i in range(1,n):
        circ.cx(qBStart+i, qAStart+i)

    circ.cx(qBStart+qBSize-1, o)

    for i in range(n-1, 1, -1):
        circ.cx(qBStart+i-1, qBStart+i)
    for i in range(1,n):
        circ.ccx(qBStart+i-1, qAStart+i-1, qBStart+i)

    circ.ccx(qBStart+qBSize-1, qAStart+qASize-1, o)
    circ.cx(qBStart+qBSize-1, qAStart+qASize-1)

    for i in range(n-1, 0, -1):
        circ.ccx(qBStart+i-1, qAStart+i-1, qBStart+i)
        circ.cx(qBStart+i-1, qAStart+i-1)

    for i in range(1, n-1):
        circ.cx(qBStart+i, qBStart+i+1)

    for i in range(n-1,0, -1):
        circ.cx(qBStart+i, qAStart+i)

    if draw == True:
        circ.draw(filename='addo_circ', output='mpl',scale=0.4,style=my_style)
    
    my_gate      = circ.to_gate()
    my_gate.name = "addo"

    if draw == True:
        circ2 = QuantumCircuit(QuantumRegister(nQBits,'d'))
        circ2.append(my_gate, [i for i in range(nQBits)])
        circ2.draw(filename='addo_gate', output='mpl',scale=0.4,style=my_style)

    return my_gate


def subo_gate(qAStart, qASize, qBStart, qBSize, o, draw=False):
    
    if qASize != qBSize:
        raise ValueError("size of Reg A not equal to size of Reg B")

    n      = qASize
    nQBits = qASize + qBSize +1
    circ   = QuantumCircuit(QuantumRegister(nQBits,'d'))

    for i in range(n):
        circ.x(qAStart + i)

    addo_g = addo_gate(qAStart, qASize, qBStart, qBSize, o)
    circ.append(addo_g, [i for i in range(2*n+1)])

    for i in range(n):
        circ.x(qAStart + i)

    if draw == True:
        circ.draw(filename='subo_circ', output='mpl',scale=0.4,style=my_style)

    my_gate      = circ.to_gate()
    my_gate.name = "subo"

    if draw == True:
        circ2 = QuantumCircuit(QuantumRegister(nQBits,'d'))
        circ2.append(my_gate, [i for i in range(nQBits)])
        circ2.draw(filename='subo_gate', output='mpl',scale=0.4,style=my_style)

    return my_gate

def cadd_gate(qAStart, qASize, qBStart, qBSize, ctrl, draw=False):
    if qASize != qBSize:
        raise ValueError("size of Reg A not equal to size of Reg B")

    n      = qBSize
    nQBits = qASize + qBSize +1
    circ   = QuantumCircuit(QuantumRegister(nQBits,'d'))

    for i in range(1,n):
        circ.cx(qBStart + i, qAStart + i)

    for i in range(n-1, 1, -1):
        circ.cx(qBStart + i - 1, qBStart + i)

    for i in range(1,n):
        circ.ccx(qBStart + i-1, qAStart + i - 1 , qBStart + i)

    circ.ccx(qBStart + qBSize - 1, ctrl, qAStart + qASize - 1)

    for i in range(n-1, 0, -1):
        circ.ccx(qBStart + i - 1, qAStart + i - 1, qBStart + i)
        circ.ccx(qBStart + i - 1, ctrl, qAStart + i - 1)

    for i in range(1, n-1):
        circ.cx(qBStart + i, qBStart + i + 1)

    for i in range(n-1,0, -1):
        circ.cx(qBStart + i, qAStart + i)

    if draw == True:
        circ.draw(filename='cadd_circ', output='mpl',scale=0.4,style=my_style)

    my_gate      = circ.to_gate()
    my_gate.name = "cadd"

    if draw == True:
        circ2 = QuantumCircuit(QuantumRegister(nQBits,'d'))
        circ2.append(my_gate, [i for i in range(nQBits)])
        circ2.draw(filename='cadd_gate', output='mpl',scale=0.4,style=my_style)

    return my_gate

def iter_gate(qreg_a_start, qreg_a_size, qreg_b_start, qreg_b_size, o, draw=False):
    if qreg_a_size != qreg_b_size:
        raise ValueError('size of Reg A not equal to size of Reg B')

    nqubits = qreg_a_size + qreg_b_size + 1
    circ = QuantumCircuit(QuantumRegister(nqubits, 'd'))

    subo = subo_gate(qreg_a_start, qreg_a_size, qreg_b_start, qreg_b_size, o)
    cadd = cadd_gate(qreg_a_start, qreg_a_size, qreg_b_start, qreg_b_size, o)

    circ.append(subo, circ.qubits)
    circ.append(cadd, circ.qubits)

    circ.x(o)

    my_gate = circ.to_gate()
    my_gate.name = 'subo'

    if draw == True:
        circ2 = QuantumCircuit(QuantumRegister(nqubits, 'd'))
        circ2.append(my_gate, [i for i in range(nqubits)])
        circ2.draw(filename='subo_gate', output='mpl', scale=0.4, style=my_style)

    return my_gate
