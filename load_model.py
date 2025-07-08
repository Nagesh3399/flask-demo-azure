from joblib import load

loaded_models = {
    "Logistic Regression": load('models/logistic_regression_model.joblib'),
    "Decision Tree": load('models/decision_tree_model.joblib'),
    "Random Forest": load('models/random_forest_model.joblib'),
    "KNN": load('models/decision_tree_model.joblib'),
    "Naive Bayes": load('models/naive_bayes_model.joblib'),
    "Gradient Boosting": load('models/gradient_boosting_model.joblib'),
}
