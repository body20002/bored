import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", port=5000, log_level="debug")
