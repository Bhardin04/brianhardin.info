FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install -e .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]