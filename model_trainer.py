import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import random

def generate_synthetic_data(num_samples=2000):
    """Generates a fake dataset of admission stats."""
    print(f"Generating {num_samples} synthetic admission samples...")
    
    data = []
    language_levels = ["B2", "C1", "C2"]
    
    for _ in range(num_samples):
        # 1. Features
        
        grade = round(random.uniform(1.0, 4.0), 1)
        # Language level
        language_level = random.choice(language_levels)
        
       
        admitted = 0 # 0 = No
        
        
        if language_level in ["C1", "C2"]:
            if grade <= 1.5:  # High chance
                admitted = 1 if random.random() < 0.95 else 0
            elif grade <= 2.5: # Good chance
                admitted = 1 if random.random() < 0.70 else 0
            elif grade <= 3.0: # Low chance
                admitted = 1 if random.random() < 0.20 else 0
        
        data.append([grade, language_level, admitted])
        
    df = pd.DataFrame(data, columns=["grade", "language_level", "admitted"])
    print("Synthetic data generated.")
    return df

def train_model(df):
    """Trains a model on the synthetic data."""
    print("Training admission prediction model...")
    
    
    df_processed = pd.get_dummies(df, columns=['language_level'], drop_first=True)
    
    
    #          language_level_C1=0, language_level_C2=1 means "C2"
    #          language_level_C1=0, language_level_C2=0 means "B2"

    # Define our features (X) and target (y)
    features = [col for col in df_processed.columns if col != 'admitted']
    X = df_processed[features]
    y = df_processed['admitted']
    
    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # --- Model Training ---
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # --- Evaluation ---
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model training complete. Test Accuracy: {acc * 100:.2f}%")
    
    return model, features

def save_model(model, features, filename="admission_model.pkl"):
    """Saves the trained model and feature list to a file."""
    

    model_data = {
        'model': model,
        'features': features
    }
    
    joblib.dump(model_data, filename)
    print(f"Model and features saved to '{filename}'.")

if __name__ == "__main__":
    data = generate_synthetic_data()
    model, features = train_model(data)
    save_model(model, features)