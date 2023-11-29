from flask import Flask, render_template, jsonify
from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from keras.models import load_model
import os
import numpy as np
import joblib

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

model_path = os.path.join(base_dir, 'static', 'assets', 'ev_model.h5')

model = load_model(model_path)

# Route to render the Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the Predictive Model page
@app.route('/predictive-model', methods=['GET', 'POST'])
def predictive_model():
    if request.method == 'POST':
        # Get the input data from the form
        total_ev_chargers = float(request.form['total_ev_chargers'])
        median_income = float(request.form['median_income'])
        total_population = float(request.form['total_population'])
        city = request.form['city']

        # Preprocess the input data similar to training data
        input_data = pd.DataFrame({
            'Total EV Chargers': [total_ev_chargers],
            'Median Income (16 and over)': [median_income],
            'Total Population': [total_population],
            'City': [city]
        })

        # Load the scaler and encoder used during training
        base_dir = os.path.abspath(os.path.dirname(__file__))
        scaler_path = os.path.join(base_dir, 'static', 'assets', 'scaler.pkl')
        encoder_path = os.path.join(base_dir, 'static', 'assets', 'encoder.pkl')
        scaler = joblib.load(scaler_path)
        encoder = joblib.load(encoder_path)

        # Preprocess numerical features (scaling)
        num_columns = ['Total EV Chargers', 'Median Income (16 and over)', 'Total Population']
        input_data[num_columns] = scaler.transform(input_data[num_columns])

        # Preprocess categorical feature (one-hot encoding)
        input_data_encoded = encoder.transform(input_data[['City']])

        # Modify the line below to use the concatenated input_data_final
        input_data_final = np.concatenate([input_data[num_columns].values, input_data_encoded], axis=1)

        # Make predictions
        prediction = model.predict(input_data_final)
        predicted_class = "EV Station Present" if prediction[0][0] >= 0.5 else "EV Station Not Present"

        return render_template('predictive_model.html', prediction=predicted_class)

    return render_template('predictive_model.html')

# Route for the Analysis page
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)