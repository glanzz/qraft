from qiskit_aer import Aer
from qiskit import transpile

class CircuitSimulator:
    SHOTS = 100
    def __init__(self, circuit) -> None:
        self.circuit = circuit
        self.circuit.measure_active()

    def simulate(self, backend=None):
        '''Simulates on ideal backend if no backend is given'''
        if not backend:
            backend = Aer.get_backend('statevector_simulator')
        self.circuit = transpile(self.circuit, backend)
        results = backend.run(self.circuit, shots=self.SHOTS)
        try:
            return {key: probability/self.SHOTS for key, probability in results.result().get_counts().items()}
        except Exception as e:
            print(e)
            return {}
