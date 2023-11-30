from flask import Flask, render_template, jsonify
from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from keras.models import load_model
import os
import numpy as np
import joblib
import pickle

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

model_path = os.path.join(base_dir, 'static', 'assets', 'model.sav')


loaded_model = pickle.load(open(model_path, "rb"))

# Route to render the Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the Predictive Model page
@app.route('/predictive-model', methods=['GET', 'POST'])
def predictive_model():
    if request.method == 'POST':
        # Get the input data from the form
        median_income = float(request.form['median_income'])
        total_population = float(request.form['total_population'])

        # Preprocess the input data similar to training data
        input_data = pd.DataFrame({
            
            'Median Income (16 and over)': [median_income],
            'Total Population': [total_population],
            
        })

        # Load the scaler and encoder used during training

        # Make predictions
        prediction = loaded_model.predict(input_data)
        # print(prediction)
        prediction = round(prediction[0])

        return render_template('predictive_model.html', prediction=prediction)

    return render_template('predictive_model.html')

# Route for the Analysis page
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)