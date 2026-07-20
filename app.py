from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# ==============================================================================
# PROSES LOADING MODEL DAN SCALER (Pastikan Anda sudah men-generate file .pkl)
# ==============================================================================
try:
    with open('model_heart.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler_heart.pkl', 'rb') as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    print("PENTING: File model_heart.pkl atau scaler_heart.pkl belum ditemukan!")
    print("Pastikan Anda sudah menjalankan script Jupyter Notebook untuk melatih model terlebih dahulu.")

@app.route('/')
def home():
    # Menampilkan halaman utama form rekam medis pasien
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # 1. Menangkap seluruh parameter numerik dan kategorikal dari form web
            age = int(request.form['age'])
            gender = int(request.form['gender'])
            hypertension = int(request.form['hypertension'])
            diabetes = int(request.form['diabetes'])
            cholesterol = int(request.form['cholesterol_level'])
            smoking = int(request.form['smoking_status'])
            alcohol = int(request.form['alcohol_consumption'])
            activity = int(request.form['physical_activity'])
            diet = int(request.form['dietary_habits'])
            stress = int(request.form['stress_level'])
            sleep = float(request.form['sleep_hours'])
            ekg = int(request.form['EKG_results'])
            
            # 2. Menyusun array sesuai dengan urutan fitur saat pelatihan model
            input_data = [
                age, gender, hypertension, diabetes, cholesterol, 
                smoking, alcohol, activity, diet, stress, sleep, ekg
            ]
            
            # 3. Transformasi data menggunakan standard scaler agar skala datanya sesuai
            data_prepared = scaler.transform([input_data])
            
            # 4. Melakukan prediksi kelas (0 atau 1) dan probabilitas persentase risiko
            prediction = model.predict(data_prepared)[0]
            probability = model.predict_proba(data_prepared)[0][1] * 100
            
            # 5. Konversi label biner menjadi teks diagnosis klinis
            if prediction == 1:
                result_text = "RISIKO TINGGI SERANGAN JANTUNG"
            else:
                result_text = "RISIKO RENDAH SERANGAN JANTUNG"
                
            # 6. Mengirim data hasil beserta variabel input spesifik ke template result.html
            return render_template('result.html', 
                                   prediction=result_text, 
                                   prob=round(probability, 2),
                                   user_age=age,
                                   user_cholesterol=cholesterol,
                                   user_sleep=sleep)
        except Exception as e:
            return f"Terjadi kesalahan pemrosesan data: {str(e)}"

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)