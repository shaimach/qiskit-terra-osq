from qiskit.aqua.translators.ising import max_cut
import  numpy as np
from qiskit.aqua.algorithms import QAOA,ExactEigensolver
from qiskit.aqua.operators import MatrixOperator,WeightedPauliOperator
from qiskit.aqua import QuantumInstance
from qiskit import BasicAer
from qiskit.aqua.components.optimizers import COBYLA, POWELL
from qiskit.quantum_info import Pauli
from qiskit.aqua import Operator
from qiskit import Aer
from qiskit.compiler import transpile
from qiskit.extensions.standard import cx,CnotGate, CzGate, HGate,h,cx, barrier
from qiskit import execute, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.circuit.instruction import Instruction
from qiskit import execute
from qiskit.providers import aer
from qiskit.aqua.operators import matrix_operator
from qiskit.tools import parallel_map
from qiskit.aqua import AquaError, aqua_globals
from scipy.optimize import minimize, basinhopping

from IsingQubitOperator import get_ising_qubitops, get_pauliList
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import QuantumError, ReadoutError
from qiskit.providers.aer.noise.errors import pauli_error
from qiskit.providers.aer.noise.errors import depolarizing_error
from qiskit.providers.aer.noise.errors import thermal_relaxation_error


class QAOA:
    def __init__(self,ising,p,qubits,useNoiseModel = False):
        self.ising = ising
        self.p = p
        self.useNoiseModel = useNoiseModel
        self.qubits = qubits
        self.register = None
        self.q = QuantumRegister(qubits)
        self.c = ClassicalRegister(qubits)
        self.register = QuantumCircuit(self.q, self.c)
        self.backend = QasmSimulator()

    def singleQAOACircuit(self,params):
        for i in range(self.qubits):
            self.register.h(self.q[i])

        h_i = {}
        j_ij = {}
        constant = 0
        for (key, value) in zip(self.ising.keys(), self.ising.values()):
            if len(key) == 1:
                h_i[key[0]] = value
            elif len(key) == 2:
                j_ij[key] = value

        for key, value in j_ij.items():
            self.register.cx(self.q[key[0]], self.q[key[1]])
            angle = value * 2 * params[0]
            self.register.rz(angle, key[1])
            self.register.cx(self.q[key[0]], self.q[key[1]])

        for i in range(self.qubits):
            self.register.rx(params[1] * 2, self.q[i])

        return self.register

    def buildQAOACircuit(self,params):
        self.register = QuantumCircuit(self.q, self.c)
        for i in  range(1,int(len(params) / 2) + 1):
            parameters = [params[i*2-1], params[i*2-2]]
            self.singleQAOACircuit(parameters)
        self.register.barrier(self.q)
        self.register.measure(self.q, self.c)
        return  self.register

    def calculateEnergy(self, transpiledCircuit):

        if self.useNoiseModel == True:

            p_reset = 0.003
            p_meas = 0.01
            p_gate1 = 0.05

            # QuantumError objects
            error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
            error_meas = pauli_error([('X', p_meas), ('I', 1 - p_meas)])
            error_gate1 = pauli_error([('X', p_gate1), ('I', 1 - p_gate1)])
            error_gate2 = error_gate1.tensor(error_gate1)

            noise_bit_flip = NoiseModel()
            noise_bit_flip.add_all_qubit_quantum_error(error_reset, "reset")
            noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
            noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
            noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cx"])

            simulator = QasmSimulator()

            job = execute(transpiledCircuit, backend=simulator, basis_gates=noise_bit_flip.basis_gates, noise_model=noise_bit_flip)
            results = job.result()
            counts = results.get_counts()

            _paulis, sgift = get_pauliList(self.ising, self.qubits)
            _basis = [(pauli[1], [i]) for i, pauli in enumerate(_paulis)]

            num_shots = sum(list(results.get_counts().values()))
            results = parallel_map(WeightedPauliOperator._routine_compute_mean_and_var,
                                   [([_paulis[idx] for idx in indices],
                                     results.get_counts())
                                    for basis, indices in _basis],
                                   num_processes=aqua_globals.num_processes)
            return results[0][0]

        else:
            _paulis, sgift = get_pauliList(self.ising, self.qubits)
            _basis = [(pauli[1], [i]) for i, pauli in enumerate(_paulis)]

            job = execute(transpiledCircuit, backend=self.backend)
            results = job.result()
            counts = results.get_counts()

            num_shots = sum(list(results.get_counts().values()))
            results = parallel_map(WeightedPauliOperator._routine_compute_mean_and_var,
                                   [([_paulis[idx] for idx in indices],
                                     results.get_counts())
                                    for basis, indices in _basis],
                                   num_processes=aqua_globals.num_processes)

            return results[0][0]




    def objectiveFunction(self,params):
        UntranspiledCircuit = self.buildQAOACircuit(params=params)

        transpiledCircuit = transpile(UntranspiledCircuit, backend=self.backend, optimization_level=1)

        qubitOp, shift = get_ising_qubitops(self.ising, self.qubits)


        avg = self.calculateEnergy(transpiledCircuit)

        return avg







