from daftlistings import Daft, Location, SearchType, PropertyType
import json

data_array = []

daft = Daft()
daft.set_location(Location.DUBLIN)
daft.set_search_type(SearchType.RESIDENTIAL_SALE)
# daft.set_property_type(PropertyType.HOUSE)

for i in range(225000, 350000, 25000):
	print(i)

	daft.set_min_price(i)
	daft.set_max_price(i+25000)

	listings = daft.search()

	print(len(listings))
	data_array.append(len(listings))


# data_array = [18,35,33,26,12]

data = {}
data = data_array
# data['b'] = ["13","14","45"]
json_string = json.dumps(data)
print(json_string)

with open('data.js', 'w') as outfile:
    outfile.write("var data = " + json_string + ";")