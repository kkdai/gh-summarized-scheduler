import os

from fastapi import FastAPI, Request
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
        result = "An error occurred while summarizing the document."
        print(result)
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
