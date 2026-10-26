FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FROZEN_PACKAGE_DIR=/app/phase16_33_frozen_model_package \
    RELEASE_GATE_FILE=/app/phase17_06_inference_api/release_gate.json

WORKDIR /app

COPY phase17_06_inference_api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY phase16_33_frozen_model_package /app/phase16_33_frozen_model_package
COPY phase17_06_inference_api /app/phase17_06_inference_api

WORKDIR /app/phase17_06_inference_api
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
