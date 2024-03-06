import numpy as np
from util import get_binary_combinations

class State:
    def __init__(self, name):
        self.name = name
        self.hamming_weight = self.get_hamming_weight()
        self.ideal_probablity = 0
        self.run_probablities = []
        self.errors = []
        self.run_prob_percentile = {
            25: 0,
            50: 0,
            75: 0
        }
        self.error_percentile = {
            25: 0,
            50: 0,
            75: 0
        }
    
    def __repr__(self) -> str:
        return f"<State name={self.name} ideal_prob={self.ideal_probablity}>"

    def get_hamming_weight(self):
        return sum(int(char) for char in self.name)

    def set_ideal_probablity(self, ideal_prob):
        self.ideal_probablity = ideal_prob
    
    def add_run_probability(self, run_prob):
        self.run_probablities.append(run_prob)
    
    def calculate_run_probability_percentile(self):
        self.run_prob_percentile = {
            25: np.percentile(self.run_probablities, 25),
            50: np.percentile(self.run_probablities, 50),
            75: np.percentile(self.run_probablities, 75),
        }
    
    def calculate_run_probability_percentile(self):
        self.run_prob_percentile = {
            25: np.percentile(self.run_probablities, 25),
            50: np.percentile(self.run_probablities, 50),
            75: np.percentile(self.run_probablities, 75),
        }
    
    def calculate_errors(self):
        self.errors = [abs(run_prob - self.ideal_probablity) for run_prob in self.run_probablities]

    def calculate_error_percentile(self):
        self.error_percentile = {
            25: np.percentile(self.errors, 25),
            50: np.percentile(self.errors, 50),
            75: np.percentile(self.errors, 75),
        }

    @classmethod
    def generate_states(cls, circuit_width) -> dict:
        return {combination: State(combination) for combination in get_binary_combinations(circuit_width)}
        
