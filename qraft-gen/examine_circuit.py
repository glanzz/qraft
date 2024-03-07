import statistics
import numpy as np  
from qiskit.providers.fake_provider import Fake5QV1
from circuit_generator import CircuitGenerator
from state_generator import generate_circuit_state
import joblib
from graph_util import generate_graph

qraft = joblib.load('qraft-1.pkl')

backend = Fake5QV1()
circuit_generator = CircuitGenerator()

stats_data= {
  "names": [],
  "medians": {
    "base": [],
    "qraft": []
  },
  "dse": {
    "base": [],
    "qraft": []
  },
  "program_error": {
    "base": [],
    "qraft": []
  }
}

for circuit_name in range(5):
  circuit_width = 3
  circuit_depth = 4
  gates = circuit_generator.get_applicable_gates(num_qubits=circuit_width,depth=circuit_depth)
  fc_circuit = circuit_generator.get_fc_circuit(circuit_width, gates)
  frc_circuit = circuit_generator.get_frc_circuit(circuit_width, gates)
  states, extras = generate_circuit_state(fc_circuit, frc_circuit, circuit_width, circuit_depth, backend)

  dominant_state = extras["dominant_state"]

  testing_data = {}
  for state in states:
    name = state.pop()
    result = state.pop()
    testing_data[name] = {
      "result": result,
      "data": state
    }

  print(testing_data)

  qraft_extra = {
    "states_errors": {},
    "program_error": 0,
    "dominant_state_error": 0
  }
  for state in testing_data:
    input = np.array(testing_data[state]["data"])
    input = input.reshape(1, -1)

    y_pred = qraft.predict(input)
    y_pred = y_pred[0]
    qraft_extra["states_errors"][state] = abs(y_pred - testing_data[state]["result"]) /100
    if state == dominant_state:
      qraft_extra["dominant_state_error"] = qraft_extra["states_errors"][state]
    qraft_extra["program_error"] += qraft_extra["states_errors"][state]  

    print(f'Predicted:{y_pred} . Actual:{testing_data[state]["result"]}')

  qraft_extra["program_error"] = qraft_extra["program_error"] / 2

  # actual, qraft
  medians = (
    statistics.median([error * 100 for error in extras["states_errors"].values()]),
    statistics.median([error * 100 for error in qraft_extra["states_errors"].values()])
  )
  dse = (
    extras["dominant_state_error"] * 100,
    qraft_extra["dominant_state_error"] * 100,
  )
  pe = (
    extras["program_error"] * 100,
    qraft_extra["program_error"] * 100
  )
  stats_data["names"].append(f"Circuit {circuit_name}")
  stats_data["medians"]["base"].append(medians[0])
  stats_data["medians"]["qraft"].append(medians[1])
  stats_data["dse"]["base"].append(dse[0])
  stats_data["dse"]["qraft"].append(dse[1])
  stats_data["program_error"]["base"].append(pe[0])
  stats_data["program_error"]["qraft"].append(pe[1])




generate_graph(
  XLABEL="Algorithms",
  YLABEL="State Error %",
  XVALUES=stats_data["names"],
  BASELINEYVALUES=stats_data["medians"]["base"],
  QRAFTYVALUES=stats_data["medians"]["qraft"]
)
generate_graph(
  XLABEL="Algorithms",
  YLABEL="Dominant State Error %",
  XVALUES=stats_data["names"],
  BASELINEYVALUES=stats_data["dse"]["base"],
  QRAFTYVALUES=stats_data["dse"]["qraft"]
)
generate_graph(
  XLABEL="Algorithms",
  YLABEL="Program Error %",
  XVALUES=stats_data["names"],
  BASELINEYVALUES=stats_data["program_error"]["base"],
  QRAFTYVALUES=stats_data["program_error"]["qraft"]
)


