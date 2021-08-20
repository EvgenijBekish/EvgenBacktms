import os
from collections import defaultdict

from fastapi import Body
from fastapi import FastAPI
from fastapi import Query
from starlette.requests import Request
from starlette.responses import Response
import psycopg2


from lessons import task_3_1

app = FastAPI()


@app.get("/task/3/1/")
def handler(name: str = Query(...)):
    result = task_3_1(name)
    return {"result": result}


numbers = defaultdict(list)


def gen_random_name():
    return os.urandom(16).hex()


def get_user(request: Request):
    return request.cookies.get("user")


def get_sum(user: str) -> int:
    sql = f"""
    SELECT n FROM numbers
    WHERE name =  '{name}'
    ;
    """
    r = execute_sql(sql)

def save_number(user: str, number: int):
    if user_exist(user):
        update_number(user, number)
    else:
        insert_new_user(user, number)



@app.post("/task/4")
def handler(
        request: Request,
        response: Response,
        data: str = Body(...),
):
    user = get_user(request) or gen_random_name()
    response.set_cookie("user", user)
    # 
    # if data == "stop":
    #     return sum(numbers[user])
    # else:
    #     assert data.isdigit()
    #     numbers[user].append(int(data))
    #     return numbers[user]

    if data == "stop":
        return get_sum(user)
    else:
        save_number(user, int(data))
        return data
