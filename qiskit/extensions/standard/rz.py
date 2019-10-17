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
Rotation around the z-axis.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate


class RZGate(Gate):
    """rotation around the z-axis."""

    def __init__(self, phi):
        """Create new rz single qubit gate."""
        super().__init__("rz", 1, [phi])

    def _define(self):
        """
        gate rz(phi) a { u1(phi) a; }
        """
        definition = []
        q = QuantumRegister(1, "q")
        rule = [
            (U1Gate(self.params[0]), [q[0]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate.

        rz(phi)^dagger = rz(-phi)
        """
        return RZGate(-self.params[0])

    def to_matrix(self):
        """Return a Numpy.array for the U3 gate."""
        lam = self.params[0]
        lam = float(lam)
        return numpy.array([[numpy.exp(-1j * lam/2), 0], [0, numpy.exp(1j * lam/2)]], dtype=complex)


def rz(self, phi, q):
    """Apply Rz to q."""
    return self.append(RZGate(phi), [q], [])


QuantumCircuit.rz = rz
