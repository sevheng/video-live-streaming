import uvicorn

# from main.app import app

if __name__ == "__main__":
    uvicorn.run('main.app:app', host="0.0.0.0", port=8000,reload=True)
