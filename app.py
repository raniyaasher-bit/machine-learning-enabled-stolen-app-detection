from flask import Flask, render_template, request, send_file
import pandas as pd
import pickle
import os

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

OUTPUT_FILE = 'output/predicted.csv'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error="No file uploaded")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No file selected")

    try:
        df = pd.read_csv(file)

        if 'Label' in df.columns:
            df.drop('Label', axis=1, inplace=True)

        predictions = model.predict(df)
        df['Prediction'] = predictions
        df['Prediction'] = df['Prediction'].map({0: 'Benign', 1: 'Malware'})

        os.makedirs('output', exist_ok=True)
        df.to_csv('output/predicted.csv', index=False)

        return render_template('index.html', message="Prediction completed successfully! You can download the result below.", download=True)

    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

@app.route('/download')
def download_file():
    return send_file(OUTPUT_FILE, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
