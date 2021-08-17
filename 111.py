from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")

async def root():
	return {"CyberPunk 2077"}



@app.get("/1/")

async def root():
	return {"2077"}
