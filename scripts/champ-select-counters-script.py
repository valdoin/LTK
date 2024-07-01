import json
import os
import requests
from bs4 import BeautifulSoup

def get_champion_names_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        exit(1)

    with open(file_path, "r", encoding="utf-8-sig") as f:
        try:
            champion_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            exit(1)

    return [champion['name'] for champion in champion_data]

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' #fake the user agent header to avoid 403 error
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to retrieve page {url}, status code: {response.status_code}")
        return None
    return BeautifulSoup(response.text, 'html.parser')

def scrape_counters_for_champions(champion_names):
    counters_data = []
    base_url = 'https://u.gg/lol/champions/'

    for name in champion_names:
        url = f"{base_url}{name}/build"
        soup = fetch_html(url)
        if soup is None:
            continue

        matchups_section = soup.find('div', class_='matchups')
        if not matchups_section:
            continue

        matchups = matchups_section.find_all('a', class_='champion-matchup')
        counters = []

        for matchup in matchups:
            champion_name_element = matchup.find('div', class_='champion-name')
            if champion_name_element:
                counters.append(champion_name_element.text.strip())

        counters_data.append({
            'champion': name,
            'counters': counters[:10] 
        })

    return counters_data

dir = os.path.dirname(__file__)
file_path_select = os.path.join(dir, "../data/champ-select-data.json")
file_path_champions = os.path.join(dir, "../data/champions-data.json")

with open(file_path_select, "r", encoding="utf-8-sig") as f:
    try:
        select_data = json.load(f)
        if select_data.get("httpStatus") == 404:
            print("You're not in champ select.")
            exit(0)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path_select}: {e}")
        exit(1)

enemy_picks = []
for action_group in select_data.get("actions", []):
    for action in action_group:
        if not action.get("isAllyAction", True) and action.get("type") == "pick":
            enemy_picks.append(action.get("championId"))

with open(file_path_champions, "r", encoding="utf-8-sig") as f:
    try:
        champion_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path_champions}: {e}")
        exit(1)

champion_names_to_scrape = []
champion_dict = {champ['id']: champ['name']for champ in champion_data}
for champ_id in enemy_picks:
    champ_name = champion_dict.get(champ_id)
    if champ_name:
        champion_names_to_scrape.append(champ_name)

champions_counters = scrape_counters_for_champions(champion_names_to_scrape)

for champ_data in champions_counters:
    print(f"Ennemy Champion: {champ_data['champion']}")
    print("Best Counters:")
    for counter in champ_data['counters']:
        print(f"  - {counter}")
    print("-----------------------------")