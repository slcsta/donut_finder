import json

f = open('response.json')

data = json.load(f)

businesses = data["businesses"]

for business in businesses:
    print("name:", business["name"])
    print("website:", business["url"])
    print("\n")
    

