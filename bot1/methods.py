import os
from typing import Optional

import httpx

from bot1.types import GetMeResponse
from bot1.types import GetWebhookInfoResponse
from bot1.types import Message
from bot1.types import Response
from bot1.types import SendMessageRequest
from bot1.types import SendMessageResponse
from bot1.types import SetWebhookResponse
from bot1.types import Type
from bot1.types import User
from bot1.types import WebhookInfo

token = os.getenv("TG_BOT_TOKEN")
url = f"https://api.telegram.org/bot{token}"
assert token, "no tg token provided"
print(f"token = {token!r}")


async def telegram_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(base_url=url) as client:
        yield client


rr_types_map = {
    "getMe": GetMeResponse,
    "getWebhookInfo": GetWebhookInfoResponse,
    "sendMessage": SendMessageResponse,
    "setWebhook": SetWebhookResponse,
}


async def api_call(
    client: httpx.AsyncClient, method: str, data: Optional[Type] = None
) -> Response:
    type = rr_types_map[method]
    payload = data.dict(exclude_unset=True) if data is not None else None
    response: httpx.Response = await client.post(f"/{method}", json=payload)
    response_as_dict = response.json()
    result = type.parse_obj(response_as_dict)

    return result


async def getMe(client: httpx.AsyncClient) -> User:
    response = await api_call(client, "getMe")
    return response.result


async def getWebhookInfo(client: httpx.AsyncClient) -> WebhookInfo:
    response = await api_call(client, "getWebhookInfo")
    return response.result


async def setWebhook(client: httpx.AsyncClient, whi: WebhookInfo) -> bool:
    response = await api_call(client, "setWebhook", data=whi)
    return response.result


async def sendMessage(
    client: httpx.AsyncClient, request: SendMessageRequest
) -> Message:
    response = await api_call(client, "sendMessage", data=request)
    return response.result
