from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Route to render the Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the Predictive Model page
@app.route('/predictive-model')
def predictive_model():
    # You can add relevant data or logic here for the Predictive Model page
    return render_template('predictive_model.html')

# Route for the Analysis page
@app.route('/analysis')
def analysis():
    # You can add relevant data or logic here for the Analysis page
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)