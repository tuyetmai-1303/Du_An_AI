from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import os

app = Flask(__name__)
CORS(app)

# 1. Cấu hình API Key Groq (Bạn lấy key miễn phí tại: https://console.groq.com/)
# Thay "YOUR_GROQ_API_KEY" bằng key của bạn
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_traffic_context():
    """Đọc dữ liệu từ Answer.txt để làm dữ liệu nền cho AI"""
    file_path = "Answer.txt"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Lỗi đọc file dữ liệu: {str(e)}"
    return "Hiện tại hệ thống chưa có dữ liệu giao thông mới nhất từ Camera và GPS."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Lấy tin nhắn từ người dùng
        data = request.json
        user_msg = data.get('message', '')

        # Lấy dữ liệu lộ trình thực tế
        traffic_data = get_traffic_context()

        # Tạo Prompt hướng dẫn AI trả lời dựa trên dữ liệu thực tế
        prompt = f"""
        Bạn là trợ lý ảo điều phối giao thông thông minh. 
        Dưới đây là dữ liệu lộ trình thực tế từ hệ thống của chúng tôi:
        
        {traffic_data}

        NHIỆM VỤ:
        - Dựa vào dữ liệu trên để chỉ đường cho người dùng.
        - Ưu tiên lộ trình có nhãn '🏆 BEST' vì đó là đường ít tắc nhất.
        - Nếu người dùng hỏi đường đi từ A đến I, hãy liệt kê các điểm đi qua và chỉ số độ tắc.
        - Trả lời ngắn gọn, thân thiện bằng tiếng Việt.
        
        CÂU HỎI NGƯỜI DÙNG: {user_msg}
        """

        # Gọi API của Groq (Sử dụng model Llama 3.1 hoặc 3.3 rất thông minh)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant", # Model này cực nhanh và miễn phí
            temperature=0.7,
        )

        reply = chat_completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {str(e)}")
        # Trả về thông báo lỗi thân thiện nếu API gặp sự cố
        if "429" in str(e):
            return jsonify({"reply": "⚠️ Hệ thống đang bận do quá nhiều yêu cầu. Vui lòng thử lại sau giây lát!"})
        return jsonify({"reply": f"❌ Có lỗi xảy ra: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)