import numpy as np
import joblib

qraft = joblib.load('qraft-1.pkl')

# Format for results dict -> {true_probability: [*inputs in order from generated file]}
results = {
  "0.0": [4,3,1,2,3,3,0,3.0,5.0,6.0,78.0,81.0,83.0,156.00000000000003,162.0,166.0],
  "13.0": [1,5,3,1,1,0,0,15.0,17.0,20.25,4.0000000000000036,5.000000000000004,7.249999999999996,8.000000000000004,10.000000000000005,14.499999999999996],
  "87.0": [1,5,3,1,1,0,1,79.75000000000001,83.0,85.0,4.0,5.0,7.250000000000001,8.000000000000004,10.000000000000005,14.499999999999996]
}

for result in results:
  input = np.array(results[result])
  input = input.reshape(1, -1)
  print("Input given:")
  print(input)

  y_pred = qraft.predict(input)

  print("Predicted:")
  print(y_pred)
  print("Actual")
  print(result)
