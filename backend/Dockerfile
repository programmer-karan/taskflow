# 1. Base Image
FROM python:3.11-slim

# 2. Environment Variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Working Directory
WORKDIR /src

# 4. Install Dependencies
# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy Source Code
COPY . .

# 6. Expose Port
EXPOSE 8000

# 7. Start Command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]