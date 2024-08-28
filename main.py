import os
from gh_tools import summarized_yesterday_github_issues
from fastapi import FastAPI
from linebot.models import TextSendMessage
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot import AsyncLineBotApi

# Load environment variables


# Initialize the FastAPI app for LINEBot
app = FastAPI()
linebot_token = os.getenv("LINE_BOT_TOKEN")
linebot_user_id = os.getenv("LINE_USER_ID")
google_api_key = os.getenv("GOOGLE_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("REPO_NAME")
repo_owner = os.getenv("REPO_OWNER")

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
if not repo_name:
    print("REPO_NAME is not set")
    exit(1)
if not repo_owner:
    print("REPO_OWNER is not set")
    exit(1)


@app.get("/")
def handle_callback():
    # get from console
    try:
        text = summarized_yesterday_github_issues(repo_owner, repo_name)
        print("--------------------")
        print(text)

        bot_token = os.getenv("LINE_BOT_TOKEN")
        user_id = os.getenv("LINE_USER_ID")
        if bot_token and user_id:
            line_bot_api = AsyncLineBotApi(
                channel_access_token=bot_token,
                http_client=AiohttpAsyncHttpClient(),
            )

            line_bot_api.push_message(user_id, TextSendMessage(text=text))
        return "OK"
    except Exception as e:
        print(e)
        return "Error"
