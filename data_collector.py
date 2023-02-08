from daftlistings import Daft, Location, SearchType, PropertyType
import json
from datetime import date

daft = Daft()

myloc = Location
daft.set_location(myloc.DUBLIN)
# for i in dir(myloc):
for i in myloc.__dict__.items():
	if not ("_" in i[0]):
		print(i[0])
		daft.set_location("DUBLIN")
exit()

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

today = date.today()

with open('data.js', 'w') as data_file:
    data_file.write("var data = " + json_string + ";")

    data_file.write(("var date = \"" + today + "\";"))