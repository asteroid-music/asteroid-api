# asteroid-api

### Setup
```bash
pip install -r requirements.txt
```

### Running
```bash
python run.py
```

Configure with environment variables:
- `MUSIC_PATH`: path to directory to keep music (directory must exist)
- `MONGO_SRV`: mongodb+srv url
- `DEBUG`: enable hot reload

For example, a full launch command could be
```bash
DEBUG=True MONGO_SRV="mongodb://localhost:27017" MUSIC_PATH="~/some/path" python run.py
```


Built with [FastAPI](https://fastapi.tiangolo.com/) and [uvicorn ASGI](https://www.uvicorn.org/).
