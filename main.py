import os
import json

from fastapi import FastAPI, Request
from linebot import LineBotApi
from linebot.models import TextSendMessage
from firebasedb import add_data  # new import
from parsers import parse_workout_record  # new import
from gh_tools import summarized_yesterday_github_issues
from langtools import summarize_with_sherpa, summarize_text

# Load environment variables
linebot_token = os.getenv("LINE_BOT_TOKEN")
linebot_user_id = os.getenv("LINE_USER_ID")
google_api_key = os.getenv("GOOGLE_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("REPO_NAME")
repo_owner = os.getenv("REPO_OWNER")

# Check if the environment variables are set
required_env_vars = {
    "LINE_BOT_TOKEN": linebot_token,
    "LINE_USER_ID": linebot_user_id,
    "GOOGLE_API_KEY": google_api_key,
    "GITHUB_TOKEN": github_token,
    "REPO_NAME": repo_name,
    "REPO_OWNER": repo_owner,
}

for var_name, var_value in required_env_vars.items():
    if not var_value:
        print(f"{var_name} is not set")
        exit(1)

# Initialize the FastAPI app for LINEBot
app = FastAPI()


# add "/" for health check
@app.get("/")
def health_check():
    print("Health Check! Ok!")
    return "OK"


@app.get("/ds")
def github_issue_daily_summarization():
    return handle_summarization(
        title="GitHub Issues",
        url=None,
        summarization_func=lambda: summarized_yesterday_github_issues(
            github_token, repo_owner, repo_name
        ),
    )


@app.post("/hn")
async def hacker_news_summarization(request: Request):
    data = await request.json()
    title = data.get("title")
    url = data.get("url")
    return handle_summarization(title, url, summarize_with_sherpa)


@app.post("/hf")
async def huggingface_paper_summarization(request: Request):
    data = await request.json()
    title = data.get("title")
    papertocode_url = data.get("url")
    url = replace_domain(papertocode_url, "paperswithcode.com", "huggingface.co")
    return handle_summarization(title, url, summarize_with_sherpa)


# 修改 webhook: 處理 POST JSON 資料（例如健身紀錄）
@app.post("/threads")
async def thread_webhook(request: Request):
    # Print request details for debugging
    print(f"Request: {request}")
    print(f"Headers: {request.headers}")

    # Get raw body
    raw_body = await request.body()
    print(f"Raw Body: {raw_body}")

    try:
        # Try to parse JSON directly from request
        data = await request.json()
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        try:
            # Attempt to clean up and parse the raw body
            body_str = raw_body.decode("utf-8")
            # Replace unescaped control characters
            body_str = (
                body_str.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
            )
            data = json.loads(body_str)
            print(f"Corrected JSON: {data}")
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            # If still fails, return error
            error_msg = f"Unable to parse request data: {str(e)}"
            print(error_msg)
            return {"status": "error", "message": error_msg}

    # Process the successfully parsed data
    if isinstance(data, dict) and "content" in data:
        parsed = parse_workout_record(data["content"])
        # 保留 CreatedAt 欄位
        if "CreatedAt" in data:
            parsed["CreatedAt"] = data["CreatedAt"]
        # 若解析結果不包含必要資料，則不儲存
        if parsed.get("running_time") is None and not parsed.get("exercises"):
            return {
                "status": "OK",
                "message": "Data did not match expected format, not stored.",
            }
        data = parsed
    elif isinstance(data, str):
        parsed = parse_workout_record(data)
        if parsed.get("running_time") is None and not parsed.get("exercises"):
            return {
                "status": "OK",
                "message": "Data did not match expected format, not stored.",
            }
        data = parsed
    else:
        # 若無法判斷格式，視為格式不符
        if data.get("running_time") is None and not data.get("exercises"):
            return {
                "status": "OK",
                "message": "Data did not match expected format, not stored.",
            }
    # 儲存資料到 Firebase 的 /threads 路徑
    add_data("/threads", data)
    return {"status": "OK", "message": "Data received and stored."}


def handle_summarization(title, url, summarization_func):
    try:
        print(f"-------{title} Summarization------")
        if url:
            print(f"Title: {title}\nURL: {url}")
        result = summarization_func() if not url else summarization_func(url)
        result = handle_summary_result(result)
        if result:
            out_text = f"{title} \n{url} \n{result}" if url else result
            send_msg(linebot_user_id, linebot_token, out_text)
        return "OK"
    except Exception as e:
        print(e)
        return "Error"


def handle_summary_result(result):
    if not result:
        print("An error occurred while summarizing the document.")
        return None
    elif len(result) > 2000:
        result = summarize_text(result)
        print(result)
    return result


def replace_domain(url, old_domain, new_domain):
    return url.replace(old_domain, new_domain)


def send_msg(linebot_user_id, linebot_token, text):
    if linebot_user_id and linebot_token:
        line_bot_api = LineBotApi(linebot_token)
        line_bot_api.push_message(linebot_user_id, TextSendMessage(text=text))
    return "OK"
