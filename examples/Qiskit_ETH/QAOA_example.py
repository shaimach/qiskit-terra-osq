from qiskit.providers.aer import QasmSimulator
from QAOA import QAOA
from scipy.optimize import minimize


#ising example with 2 qubits coupling constant is 0.5 and the constant is -0.5 and h=0 for both qubits => min energy is -1.0
isingdict ={(0,1):0.5,():-0.5}

test = QAOA(isingdict,p=1,qubits=2,us)
test.backend = QasmSimulator()



amplitudes = [0.0,0.0,0.0,0.0]
opt_result = minimize(
    test.objectiveFunction,
    amplitudes,
    method="Powell",
    options={'disp':True})

opt_energy, opt_amplitudes = opt_result.fun, opt_result.x