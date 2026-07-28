from AI_PM.notion import get_active_tasks, create_task
from AI_PM.planner import generate_daily_tasks


def main():
    print("🤖 Đang thu thập dữ liệu từ Notion...")
    current_tasks = get_active_tasks()

    print(f"📋 Tìm thấy {len(current_tasks)} task đang dang dở.")
    for t in current_tasks:
        print(f" - {t['name']} ({t['status']})")

    print("\n🧠 Đang gọi AI Project Manager suy nghĩ...")
    new_tasks = generate_daily_tasks(current_tasks)

    print("🔎 Raw tasks AI trả về:", new_tasks)

    if not new_tasks:
        print("❌ AI không đẻ ra được task nào hoặc bị lỗi.")
        return

    print(f"\n🚀 AI đã đề xuất {len(new_tasks)} task mới. Tiến hành cập nhật lên Notion...")

    success_count = 0
    for task in new_tasks:
        name = task.get("name", "Task không tên")
        if create_task(name=name):
            success_count += 1

    print(f"\n🎉 DONE! Đã tạo {success_count}/{len(new_tasks)} task lên Notion.")


if __name__ == "__main__":
    main()