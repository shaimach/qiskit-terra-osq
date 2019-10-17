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
from qiskit.circuit import Gate
from qiskit.extensions.standard.rx_pi import CX_PIGate
from qiskit.extensions.standard.rz import RZGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u3 import U3Gate


class RXGate(Gate):
    """rotation around the x-axis."""

    def __init__(self, theta):
        """Create new rx single qubit gate."""
        super().__init__("rx", 1, [theta])


    def _define(self):
        """
            gate cz a,b { h b; cx a,b; h b; }
            """
        definition = []
        q = QuantumRegister(1, "q")
        rule = [
            (RZGate(- pi / 2), [q[0]], []),
            (CX_PIGate(1), [q[0]], []),
            (RZGate(self.params[0]), [q[0]], []),
            (CX_PIGate(1), [q[0]], []),
            (RZGate(- pi / 2), [q[0]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition




def inverse(self):
        """Invert this gate.

        rx(theta)^dagger = rx(-theta)
        """
        return RXGate(-self.params[0])


def rx(self, theta, q):
    """Apply Rx to q."""
    return self.append(RXGate(theta), [q], [])


QuantumCircuit.rx = rx
