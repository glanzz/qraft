import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from skopt import BayesSearchCV
import joblib  # Use joblib from sklearn.externals in scikit-learn <= 0.23

data = pd.read_csv('circuit_simulations_data_final.csv')
X = data.drop('true_probability', axis=1)
y = data['true_probability']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

param_space = {
    'n_estimators': (10, 200),
    'max_depth': (1, 20),
    'min_samples_split': (2, 20),
    'min_samples_leaf': (1, 20),
    'max_features': (0.1, 1.0)
}

rf_regressor = RandomForestRegressor(random_state=42)

# Perform Bayesian optimization with expected improvement acquisition function
np.int = int
opt = BayesSearchCV(
    estimator=rf_regressor,
    search_spaces=param_space,
    n_iter=50,  # number of optimization steps
    random_state=42,
    cv=5,  # cross-validation folds
    scoring='neg_mean_squared_error',  # Use negative mean squared error as the scoring metric
    return_train_score=False
)
print(X_train, y_train)

opt.fit(X_train, y_train)

joblib.dump(opt.best_estimator_, 'qraft-1.pkl')

# Load the saved model
best_model = joblib.load('qraft-1.pkl')

# Make predictions on the test set using the best model
y_pred = best_model.predict(X_test)

# Calculate the accuracy of the best model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)