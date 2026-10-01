from flask import Flask, request, jsonify
from flask_cors import CORS

from db import get_additive
from ins_detector import detect_ins
from risk_engine import calculate_risk

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    POST /analyze
    Expects JSON body:
      {
        "text": "OCR Extracted Text"
      }
    
    Returns JSON body:
      {
        "detected_additives": [
          {
            "code": "...",
            "name": "...",
            "category": "...",
            "description": "...",
            "risk_score": ...,
            "high_risk_flag": ...,
            "risk_score_reason": "..."
          }
        ],
        "overall_risk_score": ...,
        "overall_risk_level": "...",
        "overall_risk_reason": "..."
      }
    """
    try:
        data = request.json or {}
        text = data.get("text", "")
        
        detected_codes = detect_ins(text)
        additives = []
        
        for code in detected_codes:
            item = get_additive(code)
            if item:
                additives.append({
                    "code": item["code"],
                    "name": item["additive_name"],
                    "category": item["category"],
                    "description": item["description"],
                    "risk_score": item["risk_score"],
                    "high_risk_flag": item["high_risk_flag"],
                    "risk_score_reason": item["risk_score_reason"]
                })
        
        score, level, reason = calculate_risk(additives)
        
        # Sort detected additives alphabetically or by code for UI consistency
        additives.sort(key=lambda x: x["code"])
        
        return jsonify({
            "detected_additives": additives,
            "overall_risk_score": score,
            "overall_risk_level": level,
            "overall_risk_reason": reason
        })
        
    except Exception as e:
        print(f"Error handling request: {e}")
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)