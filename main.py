import os
from gh_tools import summarized_yesterday_github_issues
from fastapi import FastAPI
from linebot.v3.messaging import (
    MessagingApi,
    Configuration,
    PushMessageRequest,
    TextMessage,
)

# Load environment variables
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

# Initialize the FastAPI app for LINEBot
app = FastAPI()

# Initialize the LINEBot API
configuration = Configuration(access_token=linebot_token)
api_client = MessagingApi(configuration)


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
            line_bot_api = MessagingApi(api_client)
            line_bot_api.push_message(
                PushMessageRequest(
                    to=linebot_user_id, messages=[TextMessage(text=text)]
                )
            )
        return "OK"
    except Exception as e:
        print(e)
        return "Error"
