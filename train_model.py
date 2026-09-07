import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("placement_data.csv")

# Input features
X = data.drop("placed", axis=1)

# Target/output
y = data["placed"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create the machine learning model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Test the model
prediction = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, prediction)

print("Model trained successfully!")
print("Accuracy:", round(accuracy * 100, 2), "%")

# Save the trained model
with open("placement_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")