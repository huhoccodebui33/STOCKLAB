import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def get_active_tasks():
    """
    Lấy toàn bộ task chưa Done từ Notion database.
    Có xử lý phân trang (Notion trả tối đa 100 kết quả/lần).
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    tasks = []
    payload = {"page_size": 100}

    while True:
        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code != 200:
            print("❌ Lỗi đọc Notion:", response.text)
            break

        data = response.json()
        results = data.get("results", [])

        for item in results:
            props = item.get("properties", {})

            # 1. Đọc cột "Task" (title)
            name = "Untitled"
            task_prop = props.get("Task", {})
            title_list = task_prop.get("title", [])
            if title_list:
                name = title_list[0].get("plain_text", "Untitled")

            # 2. Đọc cột "Status" - hỗ trợ cả kiểu Status lẫn Select
            status = "No Status"
            status_prop = props.get("Status", {})
            if status_prop.get("type") == "status" and status_prop.get("status"):
                status = status_prop["status"].get("name", "No Status")
            elif status_prop.get("type") == "select" and status_prop.get("select"):
                status = status_prop["select"].get("name", "No Status")

            if status != "Done":
                tasks.append({"name": name, "status": status})

        # Xử lý phân trang
        if data.get("has_more"):
            payload["start_cursor"] = data.get("next_cursor")
        else:
            break

    return tasks


def create_task(name, description="AI Project Manager tự động đề xuất."):
    """
    Tạo 1 task mới trên Notion.
    """
    if not name or not name.strip():
        print("⚠️ Bỏ qua: tên task rỗng, không tạo.")
        return False

    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Task": {"title": [{"text": {"content": name}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": description}}]
                }
            }
        ]
    }

    res = requests.post(url, headers=HEADERS, json=payload)

    if res.status_code == 200:
        print(f"✅ Đã tạo task và viết chi tiết trên Notion: {name}")
        return True
    else:
        print(f"❌ Lỗi tạo task '{name}':", res.text)
        return False