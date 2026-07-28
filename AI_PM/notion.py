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
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {} 
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print("❌ Lỗi đọc Notion:", response.text)
        return []
        
    tasks = []
    results = response.json().get("results", [])
    
    for item in results:
        props = item["properties"]
        
        # 1. Quét đúng cột tên là "Task"
        name = "Untitled"
        if "Task" in props and props["Task"]["title"]:
            name = props["Task"]["title"][0]["plain_text"]
            
        # 2. Quét đúng cột tên là "Status"
        status = "No Status"
        if "Status" in props and props["Status"].get("status"):
            status = props["Status"]["status"]["name"]

        # Chỉ lấy các task chưa Done để nạp cho AI phân tích
        if status != "Done":
            tasks.append({"name": name, "status": status})
            
    return tasks

def create_task(name, description="AI Project Manager tự động đề xuất."):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            # Tên task chính (Cột Title)
            "Task": {"title": [{"text": {"content": name}}]}
        },
        # Phần nội dung bên trong trang (Page content)
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
    else:
        print(f"❌ Lỗi tạo task: {res.text}")