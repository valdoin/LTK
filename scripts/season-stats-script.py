import json
import os

dir = os.path.dirname(__file__)
file_path1 = os.path.join(dir,"../data/games-stats-data.json")
file_path2 = os.path.join(dir,"../data/champions-data.json")

if not os.path.exists(file_path1):
    print(f"File {file_path1} not found.")
    exit(1)

if not os.path.exists(file_path2):
    print(f"File {file_path2} not found.")
    exit(1)

with open(file_path1, "r", encoding="utf-8-sig") as f:
    try:
        game_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path1}: {e}")
        exit(1)

with open(file_path2, "r", encoding="utf-8-sig") as f:
    try:
        champion_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path2}: {e}")
        exit(1)

champion_dict = {champ['id']: champ['name'] for champ in champion_data}

champion_stats = {}

for entry in game_data:
    champion_id = entry['championId']
    stats = entry['stats']['CareerStats.js']
    victory = stats['victory']
    game_played = stats['gamePlayed']
    kills = stats['kills']
    deaths = stats['deaths']
    assists = stats['assists']
    double_kills = stats['doubleKills']
    triple_kills = stats['tripleKills']
    quadra_kills = stats['quadraKills']
    penta_kills = stats['pentaKills']
    damage = stats['damage']
    cs_score = stats['csScore']
    time_played = stats['timePlayed']

    winrate = (victory / game_played) * 100 if game_played > 0 else 0

    if champion_id not in champion_stats:
        champion_stats[champion_id] = {
            'games_played': 0,
            'victories': 0,
            'kills': 0,
            'deaths': 0,
            'assists': 0,
            'double_kills': 0,
            'triple_kills': 0,
            'quadra_kills': 0,
            'penta_kills': 0,
            'damage_total': 0,
            'cs_score_total': 0,
            'time_played_total': 0
        }

    champion_stats[champion_id]['games_played'] += game_played
    champion_stats[champion_id]['victories'] += victory
    champion_stats[champion_id]['kills'] += kills
    champion_stats[champion_id]['deaths'] += deaths
    champion_stats[champion_id]['assists'] += assists
    champion_stats[champion_id]['double_kills'] += double_kills
    champion_stats[champion_id]['triple_kills'] += triple_kills
    champion_stats[champion_id]['quadra_kills'] += quadra_kills
    champion_stats[champion_id]['penta_kills'] += penta_kills
    champion_stats[champion_id]['damage_total'] += damage
    champion_stats[champion_id]['cs_score_total'] += cs_score
    champion_stats[champion_id]['time_played_total'] += time_played

for champ_id, champ_data in champion_stats.items():
    games_played = champ_data['games_played']
    victories = champ_data['victories']
    winrate = (victories / games_played) * 100 if games_played > 0 else 0
    champ_data['winrate'] = winrate
    champ_data['average_time_played'] = (champ_data['time_played_total'] / games_played) / 60000 if games_played > 0 else 0


for champ_id, champ_data in champion_stats.items():
    champ_name = champion_dict.get(champ_id, "Unknown Champion")
    print(f"Champion: {champ_name}")
    print(f"Total games played: {champ_data['games_played']:.0f}")
    print(f"Winrate: {champ_data['winrate']:.2f}%")
    print(f"Average kills: {champ_data['kills'] / champ_data['games_played']:.2f}")
    print(f"Average deaths: {champ_data['deaths'] / champ_data['games_played']:.2f}")
    print(f"Average assists: {champ_data['assists'] / champ_data['games_played']:.2f}")
    print(f"Total double kills: {champ_data['double_kills']:.0f}")
    print(f"Total triple kills: {champ_data['triple_kills']:.0f}")
    print(f"Total quadra kills: {champ_data['quadra_kills']:.0f}")
    print(f"Total penta kills: {champ_data['penta_kills']:.0f}")
    print(f"Average damage: {champ_data['damage_total'] / champ_data['games_played']:.0f}")
    print(f"Average CS score: {champ_data['cs_score_total'] / champ_data['games_played']:.0f}")
    print(f"Average game length: {champ_data['average_time_played']:.0f} mins")
    print("-----------------------------")