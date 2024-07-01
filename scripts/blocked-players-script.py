import json
import os

dir = os.path.dirname(__file__)
file_path = os.path.join(dir,"../data/blocked-players.json")

if not os.path.exists(file_path):
    print(f"File {file_path} not found.")
    exit(1)

with open(file_path, "r", encoding="utf-8-sig") as f:
    try:
        blockedPlayers = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        exit(1)
print("You've blocked the following players : \n")
for player in blockedPlayers:
    player_name = player.get("name")
    if player_name:
        print(player_name)
