import json

f = open('response.json')

data = json.load(f)

businesses = data["businesses"]

for business in businesses:
    name = business["name"]
    website = business["url"]
    rating = business["rating"]
    city = " ".join(business["location"]["city"])
    state = " ".join(business["location"]["city"])
    address = " ".join(business["location"]["display_address"])
    phone = business["display_phone"]
    print(name, website, rating)

    f.close()
    
    

