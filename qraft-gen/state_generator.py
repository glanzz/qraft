import numpy as np
from circuit_simulator import CircuitSimulator
from state import State

TOTAL_SIMULATIONS_PER_CIRCUIT = 100

def generate_circuit_state(fc_circuit, frc_circuit,  circuit_width, circuit_depth, backend):
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
      circuit_states[state].calculate_errors()
      frc_circuit_states[state].calculate_errors()
      frc_circuit_states[state].calculate_error_percentile()


  # Calculate percentile program error for FRC
  # 0000 - [1,2], 00001 - [3,4], 000010- [5,6]
  frc_program_error = [] # Sum of all the errors at each state per run
  fc_program_error = []
  for i in range(TOTAL_SIMULATIONS_PER_CIRCUIT):
      frc_program_error.append(0)
      fc_program_error.append(0)
      for state in frc_circuit_states:
          frc_program_error[i] += frc_circuit_states[state].errors[i]
          fc_program_error[i] += circuit_states[state].errors[i]
      frc_program_error[i] = frc_program_error[i]/2 # Update program error formula
      fc_program_error[i] = fc_program_error[i]/2 # Update program error formula
  
  true_state_prob = sum([circuit_states[state].ideal_probablity for state in circuit_states])

  gates_count = fc_circuit.count_ops()
  

  columns = []
  extras = {
    "ideal_prob": {},
    "states_errors": {},
    "program_error": sum(fc_program_error)/len(fc_program_error)
  }

  domainant_state = None
  for state in frc_circuit_states:
      column = [
          circuit_width, circuit_depth,gates_count.get("u1", 0), gates_count.get("u2", 0), gates_count.get("u3", 0), gates_count.get("cx", 0), frc_circuit_states[state].hamming_weight, # meidan state prob
          circuit_states[state].run_prob_percentile[25]*100, circuit_states[state].run_prob_percentile[50]*100, circuit_states[state].run_prob_percentile[75]*100,
          frc_circuit_states[state].error_percentile[25]*100, frc_circuit_states[state].error_percentile[50]*100, frc_circuit_states[state].error_percentile[75]*100,
          np.percentile(frc_program_error, 25)*100, np.percentile(frc_program_error, 50)*100, np.percentile(frc_program_error, 75)*100,  (circuit_states[state].ideal_probablity/true_state_prob)*100, state
      ]
      extras["ideal_prob"][state] = circuit_states[state].ideal_probablity
      extras["states_errors"][state] = circuit_states[state].average_error
      if not domainant_state:
        domainant_state = circuit_states[state]
      else:
        domainant_state = circuit_states[state] if circuit_states[state].ideal_probablity > domainant_state.ideal_probablity else domainant_state

      columns.append(column)

  extras["dominant_state_error"] = domainant_state.average_error
  extras["dominant_state"] = domainant_state.name
  
  return columns, extras