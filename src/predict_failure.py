import joblib

# Load trained model
model = joblib.load("models/failure_predictor.pkl")

# Example input:
# severity: 2 = ERROR
# error_count_3: recent errors count
test_input = [[2, 2]]

prediction = model.predict(test_input)

if prediction[0] == 1:
    print("⚠️ Failure likely soon")
else:
    print("✅ System stable")
