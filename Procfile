web: streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true
api: uvicorn fastapi_server:app --host=0.0.0.0 --port=${PORT:-8000}
