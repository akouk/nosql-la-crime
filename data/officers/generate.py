import json
from faker import Faker

fake = Faker()

# G=generate 100 police officers
officers = []
for _ in range(999):
    officer = {
        "badge_no": fake.random_int(min=1, max=999),
        "name": fake.name(),
        "email": fake.email(),
        "area": fake.random_int(min=1, max=21)
    }
    officers.append(officer)

# save the data to a JSON file
with open('data/officers/police_officers_data.json', 'w') as json_file:
    json.dump(officers, json_file, indent=4)

print("Police officers data saved to 'police_officers_data.json'!")

