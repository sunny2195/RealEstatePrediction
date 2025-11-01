import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, render_template
from pathlib import Path

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Load Our "Factory Products" (Model & Preprocessor) ---
# We load these ONCE at the start.
try:
    model_path = Path("artifacts/model_trainer/model.joblib")
    preprocessor_path = Path("artifacts/data_transformation/preprocessor.pkl")
    
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    
    print("--- Model and Preprocessor loaded successfully ---")
    
except FileNotFoundError:
    print("---! ERROR: Model or Preprocessor not found. ---")
    print("---! Run 'python main.py' to train the model first. ---")
    model = None
    preprocessor = None

# --- Define Routes ---

@app.route('/', methods=['GET'])
def home():
    
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
   
    if request.method == 'POST' and model and preprocessor:
        try:
            
            form_data = request.form
            
            
            data_dict = {
                'Rooms': [int(form_data.get('Rooms'))],
                'Type': [form_data.get('Type')],
                'Suburb': [form_data.get('Suburb')],
                'Method': ['S'], 
                'SellerG': ['Nelson'], 
                'Regionname': ['Southern Metropolitan'], #
                'Propertycount': [4019], 
                'Distance': [float(form_data.get('Distance'))],
                'CouncilArea': ['Other'], 
                'Sale_Year': [2017], 
                'Sale_Month': [9], 
                'Postcode': [3067] 
            }
            
            data_df = pd.DataFrame.from_dict(data_dict)
            print(f"Incoming data for prediction:\n{data_df.to_string()}")

           
            transformed_data = preprocessor.transform(data_df)
            
           
            prediction = model.predict(transformed_data)
            
      
            output = f"${prediction[0]:,.0f}"
          
            return render_template('index.html', prediction_text=f"Estimated Price: {output}")

        except Exception as e:
            print(f"Error during prediction: {e}")
            return render_template('index.html', prediction_text=f"Error: {e}")
            
   
    return render_template('index.html', prediction_text="Model not loaded. Run pipeline.")



if __name__ == "__main__":
   
    app.run(host="0.0.0.0", port=5000, debug=True)