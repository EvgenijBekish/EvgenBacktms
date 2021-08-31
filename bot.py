import httpx

def api_call(method_name: str):
    token = "1990681966:AAFteB6wmowim3mmN6c6r3XJ52yerKGamp"
    url = f"https://api.telegram.org/bot{token}/{method_name}"

    r = httpx.post(url)
    return r.json()

def getMe():
    r = api_call("getMe")
    return r

