import json
import os

file1 = "./data/owned-skins.json"
file2 = "./data/skins-data.json"

if not os.path.exists(file1):
    print(f"File {file1} not found.")
    exit(1)
if not os.path.exists(file2):
    print(f"File {file2} not found.")
    exit(1)

with open(file1, "r", encoding="utf-8-sig") as f1:
    try:
        ownedSkins = json.load(f1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file1}: {e}")
        exit(1)

with open(file2, "r", encoding="utf-8-sig") as f2:
    try:
        skinsData = json.load(f2)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file2}: {e}")
        exit(1)

rarity_values = {
    "kNoRarity": 750,
    "kEpic": 1350,
    "kLegendary": 1820,
    "kMythic": 1820,
    "kUltimate": 3250
}

total_RP_value = 0

for owned_skin in ownedSkins:
    if owned_skin['ownership']['owned'] and not owned_skin['isBase']:
        skin_name = owned_skin['name']
        skin_id = owned_skin['id']

        for skin_data in skinsData.values():
            if skin_data['id'] == skin_id and skin_data['name'] == skin_name:
                rarity = skin_data['rarity']
                total_RP_value += rarity_values.get(rarity, 0)

total_dollars_value = round(total_RP_value * 0.0077)

print(f"Total account value: {total_RP_value} RP, which is approximately {total_dollars_value}$")
