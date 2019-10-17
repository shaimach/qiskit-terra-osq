# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=invalid-name

"""
Rotation around the x-axis.
"""

import  numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u3 import U3Gate
import numpy
from qiskit.exceptions import QiskitError

class CX_PIGate(Gate):
    """rotation around the x-axis."""

    def __init__(self, theta):
        """Create new rx single qubit gate."""
        if theta % 1 != 0:
            raise QiskitError('the desired angle is not supported by the gate ')

        super().__init__("rx_pi/2", 1, [theta])


    def _define(self):
        """
        gate rx(theta) a {u3(theta, -pi/2, pi/2) a;}
        """
        definition = []
        q = QuantumRegister(1, "q")
        rule = [
            (U3Gate(self.params[0]*pi/2, -pi/2, pi/2), [q[0]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition


    def inverse(self):
        """Invert this gate.

        rx(theta)^dagger = rx(-theta)
        """
        return CX_PIGate(-self.params[0])

    def to_matrix(self):
        """Return a Numpy.array for the U3 gate."""
        lam = self.params[0]
        lam = float(lam)
        return numpy.array([[1, 0], [0, numpy.exp(1j * lam)]], dtype=complex)



def rx_pi(self, theta, q):
    """Apply Rx to q."""
    return self.append(CX_PIGate(theta), [q], [])


QuantumCircuit.rx_pi = rx_pi
