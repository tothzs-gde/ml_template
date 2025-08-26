# ML Template

## How to run locally

```
python -m venv venv
source venv/bin/activate
pip install requirements.txt
podman-compose up -d
fastapi dev src/main.py

# Test through the swagger
```

### Services

1. MiniO bucket (model storage)

username: minioadmin

password: minioadmin

URL: http://127.0.0.1:9001/

2. MLflow frontend

URL: http://127.0.0.1:8080/

3. App swagger

URL: http://127.0.0.1:8000/docs
