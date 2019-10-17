from qiskit.providers.aer import QasmSimulator
from QAOA import QAOA
from scipy.optimize import minimize

configuration = {
    'backend_name': 'qasm_simulator',
    'description': 'OpenSuperQ ETH 7 qubit chip, rev. 1, 12_15702',
    'backend_version': '0.1.0',
    'url': 'http://opensuperq.eu/',
    'sample_name': 'QUDEV_M_12_15702',
    'n_qubits': 7,
    'basis_gates': ['cz', 'rz', 'rx_pi'],
    'coupling_map': [[0, 2], [0, 3], [1, 3], [1, 4], [2, 5], [3, 5], [3, 6], [4, 6],[2, 0], [3, 0], [3, 1], [4, 1], [5, 2], [5, 3], [6, 3], [6, 4]],
    # Reduced qubit numbers by 1 compared to 20190823_OSQ_Waypoint1_experimental_parameters.pdf
    'simulator': True,
    'local': True,
    'open_pulse': False,
    'conditional': False,
    'n_registers': 1,  # Really 0, but QISKIT would not allow it, even if 'conditional' is False
    'max_shots': 10000000,
    'memory': True,
    'credits_required': False,
    'gates': [
        {'name': 'cz',
         'parameters': [],
         'coupling_map':[[0, 2], [0, 3], [1, 3], [1, 4], [2, 5], [3, 5], [3, 6], [4, 6],[2, 0], [3, 0], [3, 1], [4, 1], [5, 2], [5, 3], [6, 3], [6, 4]],
         'qasm_def': 'gate cz q1,q2 { CZ q1,q2; }'},

        {'name': 'rx_pi',
         'parameters': ['matrix'],
         'coupling_map': [[0], [1], [2], [3], [4], [5], [6]],
         'qasm_def': 'unitary(matrix) q1'},

        {'name': 'rz',
         'parameters': ['matrix'],
         'coupling_map': [[0], [1], [2], [3], [4], [5], [6]],
         'qasm_def': 'unitary(matrix) q1'},

        {'name': 'u3_eth',
         'parameters': ['matrix'],
         'coupling_map': [[0], [1], [2], [3], [4], [5], [6]],
         'qasm_def': 'unitary(matrix) q1'}

    ]
}

gates =[
    {'name': 'cz',
     'parameters': [],
     'coupling_map':[[0, 2], [0, 3], [1, 3], [1, 4], [2, 5], [3, 5], [3, 6], [4, 6],[2, 0], [3, 0], [3, 1], [4, 1], [5, 2], [5, 3], [6, 3], [6, 4]],
     'qasm_def': 'gate cZ q1,q2 { CZ q1,q2; }'},

    {'name': 'rx_pi',
     'parameters': ['matrix'],
     'coupling_map': [[0], [1], [2], [3], [4], [5], [6]],
     'qasm_def': 'unitary(matrix) q1'},

    {'name': 'rz',
     'parameters': ['matrix'],
     'coupling_map': [[0], [1], [2], [3], [4], [5], [6]],
     'qasm_def': 'unitary(matrix) q1'},

    {'name': 'u3_eth',
     'parameters': ['matrix'],
     'coupling_map': [[0], [1], [2], [3], [4], [5], [6]],
     'qasm_def': 'unitary(matrix) q1'}
]


map = [[0, 2], [0, 3], [1, 3], [1, 4], [2, 5], [3, 5], [3, 6], [4, 6],[2, 0], [3, 0], [3, 1], [4, 1], [5, 2], [5, 3], [6, 3], [6, 4]]


backend = QasmSimulator()
#backend.DEFAULT_CONFIGURATION = configuration
#backend._configuration.gates = ['cz','rx_pi','rz']
#backend._configuration.coupling_map = map
#backend._configuration.basis_gates = ['cz','rx_pi/2','rz']


isingdict ={(0,1):1.0,():-0.5}

test = QAOA(isingdict,p=1,qubits=2,useNoiseModel=True)



amplitudes = [0.0,0.0]
opt_result = minimize(
    test.objectiveFunction,
    amplitudes,
    method="Powell",
    options={'disp':True})

opt_energy, opt_amplitudes = opt_result.fun, opt_result.x

print(opt_energy, '   ', opt_amplitudes)







