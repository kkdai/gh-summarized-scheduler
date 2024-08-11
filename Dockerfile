FROM python:3.10.12

# 設定工作目錄
WORKDIR /app

# 將本地檔案複製到容器中
COPY requirements.txt requirements.txt

# 安裝依賴套件
RUN pip install -r requirements.txt

# 將應用程式程式碼複製到容器中
COPY . .

# 指定啟動命令
CMD ["python", "app.py"]