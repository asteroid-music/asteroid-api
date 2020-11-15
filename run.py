import uvicorn
import os

if __name__ == "__main__":
    hot_reload = bool(os.environ.get("DEBUG", False))
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=hot_reload)
