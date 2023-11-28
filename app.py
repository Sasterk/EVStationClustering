from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Route to render the Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the Predictive Model page
@app.route('/predictive-model')
def predictive_model():
    return render_template('predictive_model.html')

# Route for the Analysis page
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# Route for the Bios page
@app.route('/team')
def bios():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)