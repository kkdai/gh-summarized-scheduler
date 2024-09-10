import os

from fastapi import FastAPI
from fastapi import Request

from linebot import LineBotApi
from linebot.models import TextSendMessage

from gh_tools import summarized_yesterday_github_issues
from langtools import summarize_with_sherpa, summarize_text

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


@app.get("/ds")
def github_issue_daily_summarization():
    # get from console
    try:
        print("-------github_issue_daily_summarization------")
        text = summarized_yesterday_github_issues(github_token, repo_owner, repo_name)
        print(text)
        send_msg(linebot_user_id, linebot_token, text)
        return "OK"
    except Exception as e:
        print(e)
        return "Error"


@app.post("/hn")
async def hacker_news_sumarization(request: Request):
    try:
        print("-------hacker_news_sumarization------")
        data = await request.json()
        title = data.get("title")
        url = data.get("url")
        print(f"Title: {title}\nURL: {url}")
        result = summarize_with_sherpa(url)
        if not result:
            # Handle the error case, e.g., log the error or set a default message
            result = "An error occurred while summarizing the document."
            print(result)
        elif len(result) > 2000:
            result = summarize_text(result)
            print(result)
            out_text = f"{title} \n{url} \n{result}"
            send_msg(linebot_user_id, linebot_token, out_text)
        return "OK"
    except Exception as e:
        print(e)
        return "Error"


@app.post("/hf")
async def huggingface_paper_sumarziation(request: Request):
    try:
        print("-------HuggingFace_Paper_sumarization------")
        data = await request.json()
        title = data.get("title")
        papertocode_url = data.get("url")
        print(f"Papertocode URL: {papertocode_url}")
        # replace "https://paperswithcode.com/papers/2408.16046" to "https://huggingface.co/papers/2408.16046"
        url = papertocode_url.replace("paperswithcode.com", "huggingface.co")

        print(f"Title: {title}\nURL: {url}")
        result = summarize_with_sherpa(url)
        if not result:
            # Handle the error case, e.g., log the error or set a default message
            result = "An error occurred while summarizing the document."
            print(result)
        elif len(result) > 2000:
            result = summarize_text(result)
            print(result)
            out_text = f"{title} \n{url} \n{result}"
            send_msg(linebot_user_id, linebot_token, out_text)
        return "OK"
    except Exception as e:
        print(e)
        return "Error"


def send_msg(linebot_user_id, linebot_token, text):
    if linebot_user_id and linebot_token:
        line_bot_api = LineBotApi(linebot_token)
        line_bot_api.push_message(linebot_user_id, TextSendMessage(text=text))
    return "OK"
