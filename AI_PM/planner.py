import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

# Lấy API Key từ biến môi trường (.env) để tránh bị Google khóa
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def generate_daily_tasks(current_tasks):
    prompt = f"""
    Bạn là một Project Manager tài năng. Dưới đây là danh sách các công việc đang tồn đọng:
    {json.dumps(current_tasks, ensure_ascii=False)}

    Nhiệm vụ của bạn: Dựa vào tình hình trên, hãy suy nghĩ và đề xuất chính xác 2 công việc (task) MỚI cần làm hôm nay để thúc đẩy project tiến lên. Yêu cầu task phải thực tế và ngắn gọn.
    
    CHỈ TRẢ VỀ JSON ARRAY CHUẨN, ĐỊNH DẠNG:
    [
        {{"name": "Tên công việc 1"}},
        {{"name": "Tên công việc 2"}}
    ]
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt
        )
        raw_text = response.text.strip()
        
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3]
            
        new_tasks = json.loads(raw_text.strip())
        return new_tasks
        
    except Exception as e:
        print("❌ Lỗi khi gọi AI hoặc parse JSON:", e)
        return []