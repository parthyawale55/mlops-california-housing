import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# Load new data
data_path = "data/new_data.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError("Expected new data at data/new_data.csv")

df = pd.read_csv(data_path)

X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a new model
model = DecisionTreeRegressor(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Save it
joblib.dump(model, "models/best_model.pkl")
print("Model retrained and saved to models/best_model.pkl")
