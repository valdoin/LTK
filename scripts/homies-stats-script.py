import json
import os
from collections import Counter
dir = os.path.dirname(__file__)

file_path1 = os.path.join(dir,"../data/friend-counts.json")
file_path2 = os.path.join(dir,"../data/chat-logs.json" )


if not os.path.exists(file_path1):
    print(f"File {file_path1} not found.")
    exit(1)
if not os.path.exists(file_path2):
    print(f"File {file_path2} not found.")
    exit(1)

with open(file_path1, "r", encoding="utf-8-sig") as f1:
    try:
        friends_data = json.load(f1)
        num_friends = friends_data["numFriends"]
        print(f"You have {num_friends} friends.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path1}: {e}")
        exit(1)

with open(file_path2, "r", encoding="utf-8-sig") as f2:
    try:
        messages_data = json.load(f2)
        
        name_counter = Counter()
        for item in messages_data:
            name = item.get("name", "")
            if name:
                name_counter[name] += 1
        
        print("\nYour best friends are:")
        for name, count in name_counter.most_common():
            print(f"{name}: {count} messages")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path2}: {e}")
        exit(1)
