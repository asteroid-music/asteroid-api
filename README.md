# asteroid-flask

### Setup
```
pip install -r requirements.txt
```

### Running
```
flask run
```

Debug doesn't seem to work correctly in the development configuration. Would recommend exporting environment variables during development:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

See this [issue reply](https://github.com/pallets/flask/issues/3701#issuecomment-664037268).
