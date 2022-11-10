import json

f = open('response.json')

data = json.load(f)

businesses = data["businesses"]

for business in businesses:
    name = business["name"]
    website = business["url"]
    rating = business["rating"]
    address = business["location"]["address1"]
    address2 = business["location"]["address2"]
    city = business["location"]["city"]
    state = business["location"]["state"]
    zip_code = business["location"]["zip_code"] 
    display_address = business["location"]["display_address"]
    phone = business["display_phone"]
    print(name, address, city, state, zip_code) 

    f.close()


