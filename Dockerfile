FROM python:3.11

# 1. Install system dependencies (Uncommented because they are mandatory for Pillow/Torchvision)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# 2. Create the virtual environment
RUN python -m venv /opt/venv

# 3. Set the PATH to use the virtual environment binaries automatically
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# 4. Install PyTorch CPU-only into the venv
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 5. Install the rest of your requirements into the venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 6. Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]