# Sử dụng base image Python (chọn phiên bản phù hợp với code của bạn, ví dụ 3.10 hoặc 3.11)
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết (nếu có, ví dụ git, build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements trước để tận dụng Docker layer caching
COPY requirements.txt .

# Cài đặt các thư viện Python (runpod, faiss, numpy, v.v.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code của bạn (trong đó có handler.py và thư mục OpenAiServer) lên container
COPY . .

# Lệnh khởi chạy serverless handler của RunPod
CMD ["python", "-u", "handler.py"]
