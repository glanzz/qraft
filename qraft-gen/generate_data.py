import random
import numpy as np
from qiskit.providers.fake_provider import Fake5QV1
from circuit_generator import CircuitGenerator
from circuit_simulator import CircuitSimulator
from state import State



GENERATED_FILE_NAME = "circuit_simulations_data_final.csv"
TOTAL_SIMULATIONS_PER_CIRCUIT = 100
TOTAL_CIRCUITS_REQUIRED = 150
backend = Fake5QV1()


with open(GENERATED_FILE_NAME, mode="w") as generation_file:
    # Write headers to file
    generation_file.write("circuit_width,circuit_depth,u1,u2,u3,cx,hamming_weight,true_probability,25_observed_state_prob,50_observed_state_prob,75_observed_state_prob,25_frc_state_error,50_frc_state_error,75_frc_state_error,25_frc_program_error,50_frc_program_error,75_frc_program_error\n")
    circuit_generator = CircuitGenerator()

    for _ in range(TOTAL_CIRCUITS_REQUIRED):
        circuit_width = random.randint(1, 5)
        circuit_depth = random.randint(1, 5)

        gates = circuit_generator.get_applicable_gates(num_qubits=circuit_width,depth=circuit_depth)
        fc_circuit = circuit_generator.get_fc_circuit(circuit_width, gates)
        frc_circuit = circuit_generator.get_frc_circuit(circuit_width, gates)

        # Results of forward circuits
        simulator = CircuitSimulator(fc_circuit)
        circuit_states = State.generate_states(circuit_width)

        # Simulate ideal backend
        ideal_probablities = simulator.simulate()
        for prob in ideal_probablities:
            circuit_states[prob].set_ideal_probablity(ideal_probablities[prob])

        # Simulate on fake backend and calculate observed probabilites
        for i in range(TOTAL_SIMULATIONS_PER_CIRCUIT):
            results = simulator.simulate(backend)
            for state in circuit_states:
                circuit_states[state].add_run_probability(results.get(state, 0))

        # Calculate the run probablity percentile of fc_circuit
        for state in circuit_states:
            circuit_states[state].calculate_run_probability_percentile()


        # Simulate for forward reverse circuit
        frc_simulator = CircuitSimulator(frc_circuit)
        frc_circuit_states = State.generate_states(circuit_width)

        for i in range(TOTAL_SIMULATIONS_PER_CIRCUIT):
            results = frc_simulator.simulate(backend)
            for state in frc_circuit_states:
                frc_circuit_states[state].add_run_probability(
                    results.get(state, 0)
                )

        # Set ideal probability of 00000 to 1 rest all states should be zero (Anyway initialized)
        frc_circuit_states["0"*circuit_width].set_ideal_probablity(1)

        # Calculate the error percentiles for FRC States
        for state in frc_circuit_states:
            frc_circuit_states[state].calculate_errors()
            frc_circuit_states[state].calculate_error_percentile()


        # Calculate percentile program error for FRC
        # 0000 - [1,2], 00001 - [3,4], 000010- [5,6]
        frc_program_error = [] # Sum of all the errors at each state per run
        for i in range(TOTAL_SIMULATIONS_PER_CIRCUIT):
            frc_program_error.append(0)
            for state in frc_circuit_states:
                frc_program_error[i] += frc_circuit_states[state].errors[i]
        
        true_state_prob = sum([circuit_states[state].ideal_probablity for state in circuit_states])

        gates_count = fc_circuit.count_ops()
        
        for state in frc_circuit_states:
            column = [
                circuit_width, circuit_depth,gates_count.get("u1", 0), gates_count.get("u2", 0), gates_count.get("u3", 0), gates_count.get("cx", 0), frc_circuit_states[state].hamming_weight, (circuit_states[state].ideal_probablity/true_state_prob)*100,# Trur stta
                circuit_states[state].run_prob_percentile[25]*100, circuit_states[state].run_prob_percentile[50]*100, circuit_states[state].run_prob_percentile[75]*100,
                frc_circuit_states[state].error_percentile[25]*100, frc_circuit_states[state].error_percentile[50]*100, frc_circuit_states[state].error_percentile[75]*100,
                np.percentile(frc_program_error, 25)*100, np.percentile(frc_program_error, 50)*100, np.percentile(frc_program_error, 75)*100
            ]
            column_string = ",".join([str(token) for token in column])
            generation_file.write(column_string + "\n")

        print(f"Generated {_+1}th circuit data")