import requests
import json

url = "https://official-joke-api.appspot.com/random_joke"
def fetch_and_save_jokes():
    jokes = []
    for i in range(10):
        try:
            response = requests.get(url)
            response.raise_for_status()
            joke_data = response.json()
            joke = {
                "setup": joke_data.get("setup", ""),
                "punchline": joke_data.get("punchline", "")
            }
            jokes.append(joke)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении шутки #{i + 1}: {e}")
            continue
        except KeyError as e:
            print(f"Неверный формат данных шутки #{i + 1}: отсутствует поле {e}")
            continue
    try:
        with open('jokes.json', 'w', encoding='utf-8') as f:
            json.dump(jokes, f, ensure_ascii=False, indent=2)
        print(f"Успешно сохранено {len(jokes)} шуток в jokes.json")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

if __name__ == '__main__':
    fetch_and_save_jokes()
