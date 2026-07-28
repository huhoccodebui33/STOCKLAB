from .notion import get_active_tasks, create_task
from .planner import generate_daily_tasks

def main():
    print("🤖 Đang thu thập dữ liệu từ Notion...")
    current_tasks = get_active_tasks()
    
    print(f"📋 Tìm thấy {len(current_tasks)} task đang dang dở.")
    for t in current_tasks:
        print(f" - {t['name']} ({t['status']})")
        
    print("\n🧠 Đang gọi AI Project Manager suy nghĩ...")
    new_tasks = generate_daily_tasks(current_tasks)
    
    if not new_tasks:
        print("❌ AI không đẻ ra được task nào hoặc bị lỗi.")
        return
        
    print(f"\n🚀 AI đã đề xuất {len(new_tasks)} task mới. Tiến hành cập nhật lên Notion...")
    for task in new_tasks:
        create_task(name=task.get("name", "Task không tên"))
        
    print("\n🎉 DONE! Hoàn tất cập nhật Project.")

if __name__ == "__main__":
    main()