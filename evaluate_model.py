import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt


# Load dataset
data = pd.read_csv("placement_data.csv")


# Separate input and output
X = data.drop("placed", axis=1)
y = data["placed"]


# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Load trained model
with open("placement_model.pkl", "rb") as file:
    model = pickle.load(file)


# Make predictions
prediction = model.predict(X_test)


# Accuracy
accuracy = accuracy_score(y_test, prediction)

print("Model Evaluation")
print("----------------")
print("Accuracy:", round(accuracy * 100, 2), "%")


# Confusion Matrix
cm = confusion_matrix(y_test, prediction)

print("\nConfusion Matrix:")
print(cm)


# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, prediction))


# Display confusion matrix
plt.figure(figsize=(6, 5))

plt.imshow(cm)

plt.title("Placement Prediction - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.xticks([0, 1], ["Not Placed", "Placed"])
plt.yticks([0, 1], ["Not Placed", "Placed"])

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.colorbar()

plt.tight_layout()

plt.savefig("confusion_matrix.png")

plt.show()


# Feature Importance

print("\nCreating feature importance chart...")

importance = model.feature_importances_
features = X.columns

plt.figure(figsize=(10, 6))

plt.barh(features, importance)

plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Features")

plt.tight_layout()

plt.savefig("feature_importance.png", dpi=300)

plt.close()

print("Feature importance chart saved successfully!")