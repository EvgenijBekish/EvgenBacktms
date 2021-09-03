import traceback
from typing import Optional

import httpx
from fastapi import Body
from fastapi import FastAPI
from fastapi import Header
from fastapi.requests import Request
from fastapi.responses import Response

import db
import bot1
# from lessons import task_3
from users import gen_random_name
from users import get_user
from util import apply_cache_headers
from util import authorize
from util import static_response

app = FastAPI()


@app.get("/bot/about")
async def _(client: httpx.AsyncClient = bot1.Telegram):
    user = await bot1.getMe(client)
    return user


@app.get("/bot/webhook")
async def _(client: httpx.AsyncClient = bot1.Telegram):
    whi = await bot1.getWebhookInfo(client)
    return whi


@app.post("/bot/webhook")
async def _(
    client: httpx.AsyncClient = bot1.Telegram,
    whi: bot1.WebhookInfo = Body(...),
    authorization: str = Header(""),
):
    authorize(authorization)
    webhook_set = await bot1.setWebhook(client, whi)
    whi = await bot1.getWebhookInfo(client)
    return {
        "ok": webhook_set,
        "webhook": whi,
    }


@app.post("/bot/xxxx")
async def _(
    client: httpx.AsyncClient = bot1.Telegram,
    update: bot1.Update = Body(...),
):
    try:
        resp = await bot1.sendMessage(
            client,
            bot1.SendMessageRequest(
                chat_id=update.message.chat.id,
                reply_to_message_id=update.message.message_id,
                text=update.json(),
            ),
        )

        print(f"xxx\n\n{resp}\n\nxxx")
    except Exception:
        traceback.print_exc()


@app.get("/")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("index.html")


@app.get("/img")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("image.jpg")


@app.get("/js")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("index.js")


@app.post("/task/3")
async def _(name: Optional[str] = Body(default=None)):
    result = task_3(name)
    return {"data": {"greeting": result}}


@app.post("/task/4")
async def _(request: Request, response: Response, data: str = Body(...)):
    user = get_user(request) or gen_random_name()
    response.set_cookie("user", user)

    if data == "stop":
        number = await db.get_number(user)
    else:
        number = await db.add_number(user, int(data))

    return {"data": {"n": number}}
