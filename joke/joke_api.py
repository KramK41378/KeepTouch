import requests
url = "https://official-joke-api.appspot.com/random_joke"


def get_joke():
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        joke_data = response.json()
        joke = {
            "setup": joke_data.get("setup", ""),
            "punchline": joke_data.get("punchline", "")
        }
        cur_joke = joke["setup"] + '\n' + joke["punchline"]

    except Exception:
        cur_joke = ''
    return cur_joke
