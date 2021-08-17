from collections import defaultdict

from fastapi import FastAPI, Request, Body, Response
from fastapi import Query

import os

app = FastAPI()


numbers = defaultdict(list)
numbers["sadfaf"].append(1)


def gen_random_name():
	return os.urandom(16).hex()

def get_user(request: Request):
	request.cookies.get("user")

@app.post("/task/4")
def handler(
		request: Request,
		response: Response,
		data: str = Body( ... ),
):
	user = get_user(request) or gen_random_name()
	response.set_cookie("user", user)
	if data == "stop":
		return sum(numbers[user])
	else:
		assert data.isdigit()
		numbers[user].append(int(data))
	return numbers[user]

