import requests
import json

# API endpoint
url = "https://data.lacity.org/resource/2nrs-mtv8.json"

# parameters to control the limit and offset
limit = 1000  # number of rows per request (batches of 1000 records)
offset = 0    # starting point for each request
all_data = []

while len(all_data) <= 1004876: # the total records are 1004876
    # make a request with the current limit and offset
    params = {'$limit': limit, '$offset': offset}
    response = requests.get(url, params=params)
    
    # check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        break
    
    # parse the JSON response
    data = response.json()
    
    # if no more data is returned, break the loop
    if not data:
        print("No more data to fetch")
        break
    
    # append the data to the all_data list
    all_data.extend(data)
    print(f"Fetched {len(data)} rows. Total rows so far: {len(all_data)}")
    
    # update the offset for the next request
    offset += limit

# save all data to a JSON file, locally, in the same directory
with open('./data/crimes/crime_data.json', 'w') as f:
    json.dump(all_data, f)

print(f"Download completed. Total rows downloaded: {len(all_data)}")
print("Data saved to 'crime_data.json'")