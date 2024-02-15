from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model and CSV data
model = joblib.load('/Users/azyyatihanizainuddin/Desktop/MV/OpenCV/mini project/best_23.pkl')
heart_risk_data = pd.read_csv('/Users/azyyatihanizainuddin/Desktop/MV/OpenCV/mini project/heart_attack_data.csv')

# Define the prediction function with risk category logic
def predict_heart_risk(age, systolic, heart_rate, diastolic):
    risk_categories = 0
    if age >= 30:
         risk_categories += 1
    if systolic >= 180:
         risk_categories += 1
    if heart_rate >= 80:
         risk_categories += 1
    if diastolic >= 110:
         risk_categories += 1

    # Use model prediction only if at least 2 risk categories are present
    if risk_categories >= 2:
        input_row = pd.DataFrame({
            'Age': [age],
            'systolic': [systolic],
            'Heart Rate': [heart_rate],
            'diastolic': [diastolic]
        })
        input_data = pd.concat([heart_risk_data, input_row], axis=0)
        input_data = input_data.drop('Output', axis=1)
        prediction = heart_risk_data['Output']=1
    else:
        prediction = 0  # Assume low risk if less than 2 categories

    return prediction

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    systolic = int(request.form['systolic'])
    heart_rate = int(request.form['heart_rate'])
    diastolic = int(request.form['diastolic'])

    prediction = predict_heart_risk(age, systolic, heart_rate, diastolic)

    prediction_text = "Your heart risk prediction is: {}".format("high risk" if prediction == 1 else "low risk")
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for easier development