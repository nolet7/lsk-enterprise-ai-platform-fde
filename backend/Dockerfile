FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend/app /app/app
COPY middleware /app/middleware
COPY observability/otel.py /app/observability/otel.py
RUN touch /app/observability/__init__.py
COPY frontend /app/frontend
USER 65532
EXPOSE 18743
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","18743"]