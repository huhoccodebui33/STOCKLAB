import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Root của project = thư mục cha của thư mục chứa file này (AI_PM/..)
# Sửa lại số lần dirname() nếu cấu trúc thư mục của bạn khác.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Các thư mục cốt lõi cần quét, tương đối so với PROJECT_ROOT
TARGET_DIRS = ["ETL", "database", "analytics"]


def scan_project_code():
    """
    Quét code thật của project (dùng đường dẫn tuyệt đối, không phụ thuộc
    vào nơi script được gọi) để AI có ngữ cảnh chính xác.
    """
    code_summary = []
    print(f"📂 PROJECT_ROOT: {PROJECT_ROOT}")

    for d in TARGET_DIRS:
        dir_path = os.path.join(PROJECT_ROOT, d)
        exists = os.path.isdir(dir_path)
        print(f"   - {d}: {'✅ tồn tại' if exists else '❌ KHÔNG tồn tại'} ({dir_path})")

        if not exists:
            continue

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            code_summary.append(
                                f"--- File: {file_path} ---\n{content[:1500]}...\n"
                            )
                    except Exception as e:
                        print(f"⚠️ Không đọc được {file_path}: {e}")

    print(f"🔍 Tổng số file code lấy được: {len(code_summary)}")
    return "\n".join(code_summary[:5])  # Lấy mẫu một vài file, tránh vượt token


def generate_daily_tasks(current_tasks):
    project_source_code = scan_project_code()

    if not project_source_code.strip():
        print("⚠️ CẢNH BÁO: Không đọc được file code nào. AI sẽ đề xuất task KHÔNG có ngữ cảnh code thực tế.")

    prompt = f"""
Bạn là một Tech Lead kiêm Project Manager siêu cấp thông minh cho dự án Python (VNStockLab - hệ thống tài chính, ETL, dữ liệu chứng khoán).

Dưới đây là danh sách các công việc đang tồn đọng trên Notion của team:
{json.dumps(current_tasks, ensure_ascii=False)}

Và đây là một phần mã nguồn (source code) hiện tại trong các thư mục của dự án để bạn hiểu tiến độ code thực tế:
{project_source_code if project_source_code.strip() else "(Không có dữ liệu code - hãy dựa hoàn toàn vào danh sách task tồn đọng ở trên)"}

Nhiệm vụ của bạn:
- Dựa vào các task đang dở dang VÀ code thực tế hiện có, hãy phân tích xem code đang thiếu gì hoặc bước tiếp theo cần triển khai module gì (ví dụ: tối ưu pipeline ETL, fix lỗi query database, viết thêm phân tích kỹ thuật, v.v.).
- Đề xuất chính xác 2 công việc (task) MỚI, cực kỳ cụ thể, bám sát kỹ thuật của project để làm tiếp hôm nay.

CHỈ TRẢ VỀ JSON ARRAY CHUẨN, ĐỊNH DẠNG (bắt buộc dùng đúng key "name", không dùng "title"):
[
    {{"name": "Tên công việc cụ thể liên quan đến code 1"}},
    {{"name": "Tên công việc cụ thể liên quan đến code 2"}}
]

Không thêm markdown, không thêm ```json, không thêm bất kỳ text nào khác ngoài JSON array.
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        raw_text = response.text.strip()

        # Bóc tách nếu AI vẫn lỡ bọc markdown code fence
        if raw_text.startswith("```json"):
            raw_text = raw_text[len("```json"):].rstrip("`").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:].rstrip("`").strip()

        print("🔎 Raw JSON từ AI:", raw_text)

        new_tasks = json.loads(raw_text)

        # Chuẩn hoá: nếu AI lỡ trả "title" thay vì "name", tự động map lại
        normalized_tasks = []
        for t in new_tasks:
            name = t.get("name") or t.get("title") or "Task không tên"
            normalized_tasks.append({"name": name})

        return normalized_tasks

    except json.JSONDecodeError as e:
        print("❌ Lỗi parse JSON từ AI:", e)
        print("   Raw text nhận được:", raw_text if 'raw_text' in locals() else "(không có)")
        return []
    except Exception as e:
        print("❌ Lỗi khi gọi AI:", e)
        return []