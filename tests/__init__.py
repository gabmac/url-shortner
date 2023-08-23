import os

os.environ["DATABASE_TABLE"] = "shorturl"
os.environ["ENVIRONMENT"] = "local"
os.environ["ENDPOINT_URL"] = os.getenv("ENDPOINT_URL", "http://localhost:8000")
os.environ["AWS_ACCESS_KEY_ID"] = "teste"
os.environ["AWS_SECRET_ACCESS_KEY"] = "teste"
os.environ["AWS_SESSION_TOKEN"] = "teste"
os.environ["AWS_DEFAULT_REGION"] = "sa-east-1"
