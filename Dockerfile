FROM python:3.11-slim

WORKDIR /app

# Install dependencies FIRST (caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining code
COPY . .

# Start both services (Streamlit uses Render's $PORT, FastAPI uses internal 8000)
CMD ["sh", "-c", "uvicorn app.main:app --host 127.0.0.1 --port 8000 & streamlit run streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
