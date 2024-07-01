import json
import os

dir = os.path.dirname(__file__)
file1 = os.path.join(dir,"../data/owned-skins.json")
file2 = os.path.join(dir,"../data/skins-data.json")

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

rarities = {
    "kNoRarity": {"value": 750, "display_name": "No Rarity"},
    "kRare": {"value": 750, "display_name": "Rarity tier for Arcane skin line and some Mundo skins apparently (?)"},
    "kEpic": {"value": 1350, "display_name": "Epic"},
    "kLegendary": {"value": 1820, "display_name": "Legendary"},
    "kMythic": {"value": 1820, "display_name": "Mythic"},
    "kUltimate": {"value": 3250, "display_name": "Ultimate"}
}

total_RP_value = 0
nb_skins = 0
rarity_counts = {rarity: 0 for rarity in rarities.keys()}

for owned_skin in ownedSkins:
    if owned_skin['ownership']['owned'] and not owned_skin['isBase']:
        skin_name = owned_skin['name']
        skin_id = owned_skin['id']

        for skin_data in skinsData.values():
            if skin_data['id'] == skin_id and skin_data['name'] == skin_name:
                rarity = skin_data['rarity']
                total_RP_value += rarities[rarity]["value"]
                nb_skins += 1
                rarity_counts[rarity] += 1

total_dollars_value = round(total_RP_value * 0.0077)

print(f"Total account value: {total_RP_value} RP, which is approximately {total_dollars_value}$.")
print(f"You own a total of {nb_skins} skins, including:")
for rarity, count in rarity_counts.items():
    display_name = rarities[rarity]["display_name"]
    print(f"{display_name}: {count} skins")
