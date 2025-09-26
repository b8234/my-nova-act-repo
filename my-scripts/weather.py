import os
import concurrent.futures
from nova_act import NovaAct
from dotenv import load_dotenv
import unicodedata
import re

load_dotenv()

def normalize_temp(text: str) -> str:
    """
    Normalize temperature text so it always looks like 'NN°F',
    since Weather.com defaults to Fahrenheit.
    """
    if not text:
        return text
    try:
        text = text.encode("latin1").decode("utf-8")
    except Exception:
        pass
    text = unicodedata.normalize("NFKC", text)

    # Extract the numeric part of the temperature
    m = re.search(r"(-?\d+)", text)
    if m:
        return f"{m.group(1)}°F"
    return text.strip()

def check_weather(city: str):
    with NovaAct(
        starting_page="https://weather.com/",
        nova_act_api_key=os.getenv("NOVA_ACT_API_KEY"),
        headless=True
    ) as agent:
        agent.act(f"Enter '{city}' into the search box and submit")
        
        try:
            agent.act("Click the '×' to close any pop-up or cookie banner")
        except Exception:
            pass

        result = agent.act("Read the current temperature text from the results page")
        return normalize_temp(result.response)

cities = ["Boston, MA", "London, England", "Tokyo, Japan"]
results = []

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_city = {executor.submit(check_weather, city): city for city in cities}
    for future in concurrent.futures.as_completed(future_to_city):
        city = future_to_city[future]
        try:
            status = future.result()
            results.append((city, status))
        except Exception as exc:
            print(f"{city} generated an exception: {exc}")

print("\nWeather results:")
for city, status in results:
    print(f"{city} → {status}")
