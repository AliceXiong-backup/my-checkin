import json
from datetime import datetime, timedelta
import os

DATA_FILE = "checkin_data.json"
DAYS = 50

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def checkin():
    data = load_data()
    today = datetime.today().strftime("%Y-%m-%d")
    if today in data:
        print("你今天已经打过卡啦！")
    else:
        data[today] = True
        save_data(data)
        print("✅ 打卡成功！")

def view_progress():
    data = load_data()
    print("打卡记录（共 {} 天）：".format(len(data)))
    for date in sorted(data.keys()):
        print(f"{date} ✅")

def check_streak():
    data = load_data()
    dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in data.keys()])
    if not dates:
        print("你还没开始打卡呢")
        return
    streak = 0
    max_streak = 0
    prev = None
    for d in dates:
        if prev and (d - prev).days == 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
        prev = d
    print(f"最长连续打卡记录：{max_streak} 天")

def export_to_html():
    data = load_data()
    with open("status.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>我的50天打卡</title></head><body>")
        f.write("<h1>我的50天打卡挑战</h1><ul>")
        for i in range(1, 51):
            date = (datetime.today() - timedelta(days=50 - i)).strftime("%Y-%m-%d")
            status = "✅" if date in data else "❌"
            f.write(f"<li>{date}: {status}</li>")
        f.write("</ul></body></html>")
    print("✅ 已生成 status.html，你可以发给朋友啦！")

def menu():
    while True:
        print("\n📅 50天打卡挑战")
        print("1. 打卡")
        print("2. 查看记录")
        print("3. 连续打卡天数")
        print("4. 生成网页")
        print("5. 退出")
        choice = input("请输入编号：")
        if choice == "1":
            checkin()
        elif choice == "2":
            view_progress()
        elif choice == "3":
            check_streak()
        elif choice == "4":
            export_to_html()
        elif choice == "5":
            print("再见！")
            break
        else:
            print("输入错误，请重新输入。")

if __name__ == "__main__":
    menu()
