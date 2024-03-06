import numpy as np
from qiskit.circuit import QuantumRegister, QuantumCircuit
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.library.standard_gates import (IGate, U1Gate, U2Gate, U3Gate, XGate,
                                                   YGate, ZGate, HGate, SGate, SdgGate, TGate,
                                                   TdgGate, RXGate, RYGate, RZGate, CXGate,
                                                   CYGate, CZGate, CHGate, CRZGate, CU1Gate,
                                                   CU3Gate, SwapGate, RZZGate,
                                                   CCXGate, CSwapGate)

class CircuitGenerator:
    ### Custom implementation of generation of [random_circuit](https://docs.quantum.ibm.com/api/qiskit/0.24/qiskit.circuit.random.random_circuit)
    def get_applicable_gates(self, num_qubits, depth, max_operands=2, seed=None):
        """Generate random circuit of arbitrary size and form.

        This function will generate a random circuit by randomly selecting gates
        from the set of standard gates in :mod:`qiskit.extensions`. For example:

        .. jupyter-execute::

            from qiskit.circuit.random import random_circuit

            circ = random_circuit(2, 2, measure=True)
            circ.draw(output='mpl')

        Args:
            num_qubits (int): number of quantum wires
            depth (int): layers of operations (i.e. critical path length)
            max_operands (int): maximum operands of each gate (between 1 and 3)
            seed (int): sets random seed (optional)

        Returns:
            list: list of tuple with (Gate, angles, Registered Operands)

        Raises:
            CircuitError: when invalid options given
        """

        if max_operands < 1 or max_operands > 2:
            raise CircuitError("max_operands must be between 1 and 2")

        one_q_ops = [U1Gate, U2Gate, U3Gate] # Excluded , XGate, YGate, ZGate, HGate, SGate, SdgGate, TGate, TdgGate, RXGate, RYGate, RZGate, IGate
        one_param = [U1Gate] # Not included RZZGate, CU1Gate, CRZGate, RXGate, RYGate, RZGate
        two_param = [U2Gate]
        three_param = [U3Gate] # Not included CU3Gate
        two_q_ops = [CXGate] # Not included CYGate, CZGate, CHGate, CRZGate, CU1Gate, CU3Gate, SwapGate, RZZGate
        # three_q_ops = [CCXGate, CSwapGate] # Not allowing 3 Quibits to be generated

        qr = QuantumRegister(num_qubits, 'q')
        #qc = QuantumCircuit(num_qubits)

        if seed is None:
            seed = np.random.randint(0, np.iinfo(np.int32).max)
        rng = np.random.default_rng(seed)


        gates_applied = []
        # apply arbitrary random operations at every depth
        for _ in range(depth):
            # choose either 1 or 2 qubits for the operation NOTE: Excluded 3 qubit operations on purpose
            remaining_qubits = list(range(num_qubits))
            while remaining_qubits:
                max_possible_operands = min(len(remaining_qubits), max_operands)
                num_operands = rng.choice(range(max_possible_operands)) + 1
                rng.shuffle(remaining_qubits)
                operands = remaining_qubits[:num_operands]
                remaining_qubits = [q for q in remaining_qubits if q not in operands]
                if num_operands == 1:
                    operation = rng.choice(one_q_ops)
                elif num_operands == 2:
                    operation = rng.choice(two_q_ops)
                '''elif num_operands == 3:
                    operation = rng.choice(three_q_ops)'''
                if operation in one_param:
                    num_angles = 1
                elif operation in two_param:
                    num_angles = 2
                elif operation in three_param:
                    num_angles = 3
                else:
                    num_angles = 0
                angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
                register_operands = [qr[i] for i in operands]
                #op = operation(*angles)

                gates_applied.append((operation, angles, register_operands))
                #qc.append(op, register_operands)


        return gates_applied
    
    def get_fc_circuit(self, circuit_width, applicable_gates):
        '''Provides the forward circuit applying the given gates'''
        qc = QuantumCircuit(circuit_width)
        for gate in applicable_gates:
            self.__apply_gate(qc, gate)
        return qc
    
    def __apply_gate(self, qc: QuantumCircuit, gate):
        '''Applies the gate operation to the given circuit'''
        operation = gate[0]
        angles = gate[1]
        register_operands = gate[2]
        qc.append(operation(*angles), register_operands)
    
    def get_frc_circuit(self, circuit_width, applicable_gates:list):
        '''Provides the forward circuit applying the given gates'''
        frc_circuit = self.get_fc_circuit(circuit_width=circuit_width, applicable_gates=applicable_gates)
        # Apply gate operations in reverse to the fc circuit
        for gate in reversed(applicable_gates):
            self.__apply_gate(frc_circuit, gate=gate)
        return frc_circuit
