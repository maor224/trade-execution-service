# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    echo "export PATH=$HOME/.local/bin:$PATH" >> /etc/environment

# Copy pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN . /etc/environment && poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Expose port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
