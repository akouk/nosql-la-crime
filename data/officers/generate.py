import json
from faker import Faker

fake = Faker()

# generate 1000 police officers
officers = []
for _ in range(9999):
    officer = {
        "badge_no": fake.random_int(min=1, max=99999),
        "name": fake.name(),
        "email": fake.email(),
        "area": fake.random_int(min=1, max=21)
    }
    officers.append(officer)

# save the data to a JSON file, loccaly, in the same directory
with open('data/officers/officers_data.json', 'w') as json_file:
    json.dump(officers, json_file, indent=4)

print("Police officers data saved to 'police_officers_data.json'")

