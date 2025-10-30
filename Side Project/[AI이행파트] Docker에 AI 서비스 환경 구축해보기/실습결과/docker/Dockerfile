# Multi-stage build for AI Sentiment Analysis Service
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim AS production

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Install only necessary runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY src/ ./src/
COPY docker/entrypoint.sh ./
COPY docker/healthcheck.sh ./

# Set permissions
RUN chmod +x entrypoint.sh healthcheck.sh \
    && chown -R app:app /app

# Set Python path
ENV PYTHONPATH=/app/src

# Set model cache directory with write permissions
ENV TRANSFORMERS_CACHE=/tmp/models
ENV HF_HOME=/tmp/models

# Create cache directory with proper permissions
RUN mkdir -p /tmp/models && chmod 777 /tmp/models

# Switch to non-root user
USER app

# Add .local/bin to PATH for user-installed packages
ENV PATH=/home/app/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ./healthcheck.sh

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]