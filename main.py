import uvicorn
import app

uvicorn.run(app.app, host="127.0.0.1", port=8000)