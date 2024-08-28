import os
from gh_tools import summarized_yesterday_github_issues
from fastapi import FastAPI
from linebot import LineBotApi
from linebot.models import TextSendMessage

# Load environment variables


# Initialize the FastAPI app for LINEBot
app = FastAPI()
linebot_token = os.getenv("LINE_BOT_TOKEN")
linebot_user_id = os.getenv("LINE_USER_ID")
google_api_key = os.getenv("GOOGLE_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")

# check if the environment variables are set
if not linebot_token:
    print("LINE_BOT_TOKEN is not set")
    exit(1)
if not linebot_user_id:
    print("LINE_USER_ID is not set")
    exit(1)
if not google_api_key:
    print("GOOGLE_API_KEY is not set")
    exit(1)
if not github_token:
    print("GITHUB_TOKEN is not set")
    exit(1)


@app.get("/")
def handle_callback():
    # get from console
    try:
        text = summarized_yesterday_github_issues()
        print("--------------------")
        print(text)

        bot_token = os.getenv("LINE_BOT_TOKEN")
        user_id = os.getenv("LINE_USER_ID")
        if bot_token and user_id:
            line_bot_api = LineBotApi(bot_token)
            line_bot_api.push_message(user_id, TextSendMessage(text=text))
        return "OK"
    except Exception as e:
        print(e)
        return "Error"
