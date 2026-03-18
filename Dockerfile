FROM python:3.11-slim

WORKDIR /app

# Install dependencies FIRST (caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining code
COPY . .

# Start Streamlit (Render injects $PORT automatically)
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
