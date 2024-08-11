# GCP Scheduler

這是一個使用 Google Cloud Platform (GCP) Scheduler 的範例專案，主要功能是自動化地從 GitHub Issues 中提取資料並生成摘要。

## 目錄

- [專案介紹](#專案介紹)
- [功能](#功能)
- [安裝](#安裝)
- [使用方法](#使用方法)
- [環境變數](#環境變數)
- [貢獻](#貢獻)
- [授權](#授權)

## 專案介紹

這個專案使用了多種技術，包括 LangChain、Google Generative AI 和 GitHub Issues Loader，來自動化地從 GitHub Issues 中提取資料並生成摘要。摘要會以簡短的文章形式呈現，並附上原文的 URL 連結，方便回顧。

## 功能

- 從指定的 GitHub Repository 中提取 Issues 資料
- 使用 Google Generative AI 生成摘要
- 自動化處理和生成摘要文章

## 安裝

1. 克隆這個倉庫到本地端：

    ```bash
    git clone https://github.com/yourusername/gcp-scheduler.git
    cd gcp-scheduler
    ```

2. 建立並啟動虛擬環境：

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
    ```

3. 安裝所需的 Python 套件：

    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

1. 設定環境變數：

    ```bash
    export GITHUB_TOKEN=your_github_token
    export GOOGLE_API_KEY=your_gemini_api_key
    ```

2. 執行主程式：

    ```bash
    python main.py
    ```

    程式會自動從 GitHub Issues 中提取前一天資料並生成摘要，並在終端機中顯示結果。

## 環境變數

- `GITHUB_TOKEN`: 用於訪問 GitHub API 的個人訪問令牌。
- `GOOGLE_API_KEY`: 用於產生相關 LLM 總結與相關的推薦文字，作為使用。

## 貢獻

歡迎任何形式的貢獻！請先閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多資訊。

## 授權

這個專案使用 [MIT 授權](LICENSE)。
