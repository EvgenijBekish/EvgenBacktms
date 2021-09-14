import json

from random import choice
from string import ascii_lowercase
from typing import Optional
from typing import Tuple
from typing import Union

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from task4.models import Number


def get_user_name(request: HttpRequest) -> Optional[str]:
    name = request.headers.get("x-user") or None
    return name


def create_new_user_name() -> str:
    def word() -> str:
        return "".join(choice(ascii_lowercase) for _ in range(6))

    return "-".join(word() for _ in "123")


def set_user_name(response: HttpResponse, name: str) -> None:
    response.headers["x-user"] = name


def add_number(name: str, number: int):
    obj: Tuple[Number, bool] = Number.objects.get_or_create(name=name)
    rec, _created = obj
    rec.n += number
    rec.save()
    return rec.n


def validate_number(number: int) -> None:
    lower_bound, upper_bound = -100, 100
    if not (lower_bound <= number <= upper_bound):
        raise ValueError(
            f"number {number} is not in range {(lower_bound, upper_bound)}"
        )


def parse_payload(request: HttpRequest) -> Union[str, int, None]:
    if not request.body:
        raise ValueError("non-empty body is required")

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError as err:
        raise ValueError(f"malformed payload: {request.body!r} ({err})") from err

    if isinstance(payload, int):
        validate_number(payload)
    elif payload != "stop":
        raise ValueError(
            f"value {payload!r} is not acceptable: MUST be either int, or 'stop'"
        )

    return payload


class UnprocessableEntityResponse(JsonResponse):
    status_code = 422


@csrf_exempt
@require_http_methods(["POST"])
def task(request: HttpRequest) -> HttpResponse:
    name = get_user_name(request)
    if not name:
        return UnprocessableEntityResponse("header X-USER is not set", safe=False)

    try:
        payload = parse_payload(request)
    except ValueError as err:
        response = UnprocessableEntityResponse(str(err), safe=False)
    else:
        if isinstance(payload, int):
            current = add_number(name, payload)
        elif payload == "stop":
            current = add_number(name, 0)
        else:
            current = None

        response = JsonResponse(
            current,
            safe=False,
        )

    set_user_name(response, name)
    return response