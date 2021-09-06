# import uvicorn
#
# from alexcode import app
#
# uvicorn.run(
#     app,
#     host="0.0.0.0",
#     port=8000,
#     log_level="debug",
# )


import uvicorn

from alexcode import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
    )