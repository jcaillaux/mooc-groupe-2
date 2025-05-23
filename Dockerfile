# Stage 1: Build Vue frontend
FROM node:lts-alpine AS frontend-build

# Set working directory and copy Vue project files
WORKDIR /app
COPY frontend/front-mooc /app/frontend
WORKDIR /app/frontend

# Verify the files are correctly copied
RUN ls -la
RUN cat package.json || echo "package.json not found"

# Install dependencies and build
RUN npm install
RUN npm run build

# Stage 2: Build Python backend
FROM python:3.12-slim AS backend-build

WORKDIR /app
RUN mkdir -p /.cache/huggingface /.cache/torch /.cache/sentence_transformers && \
    chmod -R 777 /.cache

# Set all HF-related environment variables
ENV HF_HOME=/.cache/huggingface
ENV HF_DATASETS_CACHE=/.cache/huggingface/datasets
ENV TRANSFORMERS_CACHE=/.cache/huggingface/transformers
ENV TORCH_HOME=/.cache/torch
ENV SENTENCE_TRANSFORMERS_HOME=/.cache/sentence_transformers
COPY requirements.txt .
#  COPY .env .
COPY config.py .
RUN pip install --no-cache-dir --upgrade pip

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final image

# Copy built frontend files from frontend-build
COPY --from=frontend-build /app/frontend/dist /app/app/templates  

# Copy application code
COPY ./app /app/app
COPY ./data /app/data
COPY config.py /app/

# Expose the port for Hugging Face
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
