import random
from qiskit.providers.fake_provider import Fake5QV1
from circuit_generator import CircuitGenerator
from state_generator import generate_circuit_state



GENERATED_FILE_NAME = "circuit_simulations_data_final.csv"
TOTAL_CIRCUITS_REQUIRED = 300
backend = Fake5QV1()


with open(GENERATED_FILE_NAME, mode="w") as generation_file:
    # Write headers to file
    generation_file.write("circuit_width,circuit_depth,u1,u2,u3,cx,hamming_weight,25_observed_state_prob,50_observed_state_prob,75_observed_state_prob,25_frc_state_error,50_frc_state_error,75_frc_state_error,25_frc_program_error,50_frc_program_error,75_frc_program_error,true_probability,state_name\n")
    circuit_generator = CircuitGenerator()
    

    for _ in range(TOTAL_CIRCUITS_REQUIRED):
        circuit_width = random.randint(1, 5)
        circuit_depth = random.randint(1, 5)
        gates = circuit_generator.get_applicable_gates(num_qubits=circuit_width,depth=circuit_depth)
        fc_circuit = circuit_generator.get_fc_circuit(circuit_width, gates)
        frc_circuit = circuit_generator.get_frc_circuit(circuit_width, gates)
        columns, ext = generate_circuit_state(fc_circuit, frc_circuit, circuit_width, circuit_depth, backend)
        print(ext)
        for column in columns:
            generation_file.write(",".join([str(token) for token in column]) + "\n")

        print(f"Generated {_+1}th circuit data")