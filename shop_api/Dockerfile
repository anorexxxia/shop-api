FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    proto/auth.proto
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]