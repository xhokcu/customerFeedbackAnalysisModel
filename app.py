from flask import Flask, request, jsonify
from transformers import pipeline
import pandas as pd
from flask_cors import CORS

# Flask uygulamasını başlat
app = Flask(__name__)
CORS(app)

# Hugging Face Sentiment Analysis pipeline'ını başlat
sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

# Excel dosyasını işleme ve sentiment analizi gerçekleştirme fonksiyonu
def process_excel(file):
    try:
        data = pd.read_excel(file)
    except Exception as e:
        return {"error": f"Excel dosyası okunurken hata oluştu: {str(e)}"}

    if "feedback" not in data.columns:
        return {"error": "Excel dosyasında 'feedback' adlı sütun bulunamadı."}
    
    feedbacks = data["feedback"].astype(str).tolist()
    
    try:
        results = sentiment_pipeline(feedbacks)
        data["sentiment"] = [result["label"] for result in results]
        data["score"] = [result["score"] for result in results]
        return data
    except Exception as e:
        print(f"hataaa {(e)}")
        return {"error": f"Sentiment analizi sırasında hata oluştu: {str(e)}"}
    
@app.route("/")
def home():
    return "Sentiment Analysis API çalışıyor! Dosya yüklemek için /upload endpoint'ini kullanın."

# Backend API endpoint: Excel dosyasını yükleme ve analiz etme
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Dosya yüklenmedi."}), 400
    
    file = request.files["file"]
    if not file:
        return jsonify({"error": "Geçersiz dosya."}), 400

    processed_data = process_excel(file)
    
    if "error" in processed_data:
        return jsonify({"error": processed_data["error"]}), 400

    return jsonify(processed_data.to_dict(orient="records"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)