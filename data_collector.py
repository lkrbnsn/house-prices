from daftlistings import Daft, Location, SearchType, PropertyType
import json
import datetime
# import pandas as pd
import numpy as np
import statistics

# test_price_list = [450000, 650000, 450000, 390000, 625000, 360000, 360000, 420000, 260000, 59000, 360000, 165000, 270000, 279500, 120000, 239950, 330000, 350000, 365000, 469950, 395000, 225000, 165000, 275000, 200000, 380000, 90000, 497500, 285000, 175000, 325000, 240000, 435000, 235000, 265000, 35000, 295000, 895000, 290000, 89000, 285000, 79000, 299500, 175000, 280000, 395000, 200000, 1850000, 285000, 480000, 270000, 525000, 595000, 750000, 260000, 70000, 179950, 260000, 450000, 275000, 205000, 150000, 125000, 205000, 275000, 145000, 485000, 165000, 240000, 249000, 135000, 305000, 160000, 350000, 950000, 125000, 225000, 150000, 500000, 950000, 430000, 950000, 300000, 125000, 800000, 475000, 340000, 349950, 275000, 165000, 295000, 200000, 425000, 150000, 580000, 450000, 450000, 365000, 255000, 295000, 139500, 380000, 130000, 225000, 385000, 155000, 250000, 299000, 190000, 950000, 375000, 599950, 339500, 275000, 415000, 75000, 175000, 150000, 299950, 330000, 220000, 449500, 50000, 285000, 299950, 575000, 325000, 355000, 275000, 275000, 380000, 595000, 325000, 190000, 280000, 345000, 450000, 95000, 750000, 450000, 270000, 25000, 149000, 265000, 315000, 135000, 190000, 375000, 175000, 310000, 450000, 475000, 295000, 220000, 300000, 285000, 4800000, 8500000, 8500000, 225000, 250000, 595000, 290000, 225000, 225000, 230000, 450000, 449000, 475000, 225000, 299500, 375000, 375000, 8500000, 200000, 140000, 325000, 160000, 320000, 350000, 275000, 150000, 190000, 300000, 265000, 180000, 600000, 599950, 595000, 250000, 290000, 950000, 195000, 330000, 350000, 55000]
# test_price_array = np.array(test_price_list)
# bins = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]
# print(len(test_price_list))

# for i in bins:
# 	total_less_than = test_price_array[test_price_array <= i]
# 	total = total_less_than[total_less_than > (i-100000)]
# 	print(total.size)
# print(test_price_array[test_price_array > 1000000].size)

# exit()

location_list = ["all",
Location.ANTRIM,
Location.ARMAGH,
Location.CAVAN,
Location.CARLOW,
Location.CLARE,
Location.CORK,
Location.DERRY,
Location.DOWN,
Location.DONEGAL,
Location.DUBLIN,
Location.FERMANAGH,
Location.GALWAY,
Location.KERRY,
Location.KILDARE,
Location.KILKENNY,
Location.LAOIS,
Location.MAYO,
Location.MEATH,
Location.MONAGHAN,
Location.LEITRIM,
Location.LIMERICK,
Location.LONGFORD,
Location.LOUTH,
Location.OFFALY,
Location.ROSCOMMON,
Location.SLIGO,
Location.TIPPERARY,
Location.TYRONE,
Location.WATERFORD,
Location.WESTMEATH,
Location.WEXFORD,
Location.WICKLOW]

property_type_list = ["any",
PropertyType.HOUSE,
PropertyType.DETACHED_HOUSE,
PropertyType.SEMI_DETACHED_HOUSE,
PropertyType.TERRACED_HOUSE,
PropertyType.END_OF_TERRACE_HOUSE,
PropertyType.TOWNHOUSE,
PropertyType.DUPLEX,
PropertyType.BUNGALOW,
PropertyType.APARTMENT,
PropertyType.STUDIO_APARTMENT,
PropertyType.SITE
]

bins = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]
step_size = bins[1] - bins[0]

# Pull in the data from the last 6 days, we'll need it
old_json_data_list = [] # List to hold each of the dictionaries
date_list = [] # List to hold each of the dates for display purposes
for i in range(6,0,-1):
	old_filename = "data/data_" + str(datetime.date.today() - datetime.timedelta(days = i)) + ".json"
	date_list.append((datetime.date.today() - datetime.timedelta(days = i)).strftime("%d %b"))
	print(old_filename)
	with open(old_filename, 'r') as old_data_file:
		first_line = old_data_file.readline()
		first_line = (first_line.split("\'"))[1].split("\'")[0]
		old_json_data = json.loads(first_line)
		old_json_data_list.append(old_json_data)

date_list.append(datetime.date.today().strftime("%d %b"))

# Dictionary to hold all the data we're going to write to the json file
data = {}

for location in location_list:
	# Create the parameters in the dictionary to write our array to
	if (location == "all"):
		json_location = "all"
	else:
		json_location = location.value["displayValue"]
	data[json_location] = {}
	
	for property_type in property_type_list:

		print("Getting data for", property_type, "in", location)
		daft = Daft()
		daft.set_search_type(SearchType.RESIDENTIAL_SALE)
		if (location != "all"):
			daft.set_location(location)
		if (property_type != "any"):
			daft.set_property_type(property_type)
		daft._paging["from"] = 0 # Workaround to fix bug in daftlistings

		print(daft._filters)

		listings = daft.search()
		price_list = []
		for listing in listings:
			price = listing.price
			# Remove all unwanted characters and convert to int
			price = price.replace("€", "")
			price = price.replace(",", "")
			price = price.replace("AMV: ", "")
			if(price.isdigit()):
				price_list.append(int(price))

		print(len(price_list))

		# Convert to numpy array so we can calculate the amounts for each bin
		data_list = []
		price_array = np.array(price_list)
		for i in bins:
			total_less_than = price_array[price_array <= i]
			total = total_less_than[total_less_than > (i-step_size)]
			data_list.append(total.size)
		data_list.append(price_array[price_array > bins[-1]].size) # Get the final amound, > last bin


		if (property_type == "any"):
			json_property_type = "any"
		else:
			json_property_type = property_type.value

		# Write to the dictionary
		data[json_location][json_property_type] = {}
		data[json_location][json_property_type]["bins"] = data_list
		data[json_location][json_property_type]["total"] = len(price_list)
		if len(price_list) != 0:
			data[json_location][json_property_type]["mean"] = round(statistics.mean(price_list), 0)
		else:
			data[json_location][json_property_type]["mean"] = 0

		# Get the seven day price list from the old data
		seven_day_price_list = []
		for i in old_json_data_list:
			seven_day_price_list.append(i[json_location][json_property_type]["mean"])

		# Seventh day is today
		seven_day_price_list.append(data[json_location][json_property_type]["mean"])

		data[json_location][json_property_type]["seven_day"] = seven_day_price_list


json_string = json.dumps(data)
print(json_string)

today = datetime.date.today().strftime("%d %B %Y")

filename = "data/data_" + str(datetime.date.today())  + ".json"

with open(filename, 'w') as data_file:
    data_file.write("var data = \'" + json_string + "\';\n")
    data_file.write(("var date = \"" + today + "\";\n"))
    data_file.write(("var date_list = " + str(date_list) + ";\n"))


with open("data/data.json", 'w') as data_file:
    data_file.write("var data = \'" + json_string + "\';\n")
    data_file.write(("var date = \"" + today + "\";\n"))
    data_file.write(("var date_list = " + str(date_list) + ";\n"))