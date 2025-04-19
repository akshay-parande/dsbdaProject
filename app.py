import os
from flask import Flask, render_template, request
import pickle
import numpy as np
from db_config import get_connection

app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/', methods=["GET", "HEAD"])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the user
    hours = float(request.form['hours'])
    attendance = int(request.form['attendance'])
    internal = int(request.form['internal'])

    # Prepare the input data for prediction
    input_data = np.array([[hours, attendance, internal]])
    prediction = float(model.predict(input_data)[0])  # Convert numpy.float64 → float

    # Save prediction data to DB
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                hours_studied FLOAT,
                attendance FLOAT,
                internal_marks FLOAT,
                predicted_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                hours_studied FLOAT,
                attendance FLOAT,
                internal_marks FLOAT,
                predicted_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

        cursor.execute("""
        INSERT INTO predictions (hours_studied, attendance, internal_marks, predicted_score)
        VALUES (%s, %s, %s, %s)
        """, (hours, attendance, internal, prediction))

        conn.commit()

    except Exception as e:
        print("Database error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    # Return the result back to the user
    return render_template('index.html', result=round(prediction, 2),
                           hours=hours, attendance=attendance, internal=internal)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
