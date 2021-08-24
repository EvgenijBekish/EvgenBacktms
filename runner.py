import uvicorn

from alexcode import app

uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    log_level="debug",
)
