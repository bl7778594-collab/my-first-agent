import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors


def main():
    # 加载与脚本同级的 .env 文件
    load_dotenv(Path(__file__).resolve().with_name(".env"))
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("请在同级目录的 .env 文件中配置 GEMINI_API_KEY。")

    # 程序退出时自动关闭客户端
    with genai.Client(api_key=api_key) as client:
        # 在循环外创建会话，自动保留本次运行中的对话上下文
        chat = client.chats.create(model="gemini-2.5-flash")
        print("Gemini 对话已启动，输入 exit 退出。")

        while True:
            try:
                user_input = input("你：").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n对话已结束。")
                break

            if user_input.lower() == "exit":
                print("对话已结束。")
                break
            if not user_input:
                continue

            try:
                # 使用同一个会话发送消息，延续上下文
                response = chat.send_message(user_input)
                print(f"Gemini：{response.text or '未收到文本回复。'}\n")
            except errors.APIError as error:
                print(f"请求失败：{error}\n")


if __name__ == "__main__":
    main()
