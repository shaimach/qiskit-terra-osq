import  numpy as np
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.quantum_info import Pauli

def get_pauliList(ising,qubits):
    h_i = {}
    j_ij = {}
    constant = 0
    for (key, value) in zip(ising.keys(), ising.values()):
        if len(key) == 1:
            h_i[key[0]] = value
        elif len(key) == 2:
            j_ij[key] = value
        elif len(key) == 0:
            constant = value

    num_nodes = qubits
    pauli_list = []

    for key, value in j_ij.items():
        xp = np.zeros(num_nodes, dtype=np.bool)
        zp = np.zeros(num_nodes, dtype=np.bool)
        zp[key[0]] = True
        zp[key[1]] = True
        pauli_list.append([value, Pauli(zp, xp)])
    for key, value in h_i.items():
        xp = np.zeros(num_nodes, dtype=np.bool)
        zp = np.zeros(num_nodes, dtype=np.bool)
        zp[key] = True
        pauli_list.append([value, Pauli(zp, xp)])

    return pauli_list, constant


def get_ising_qubitops(ising,qubits):
    pauli_list, constant = get_pauliList(ising,qubits)

    return WeightedPauliOperator(paulis=pauli_list), constant

isingdict ={(0,1):0.5,():-0.5}
qubitOp, shift  = get_ising_qubitops(isingdict,2)