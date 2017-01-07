# Recipe database from https://github.com/fictivekin/openrecipes

# Set key values
num_choices = 5		# Number of recipes to choose from the subpopulation

import json
from random import sample
import webbrowser

data = []

with open('recipeitems-latest.json') as data_file:    
    for line in data_file:
	    data.append(json.loads(line))

# Prep time is in the format "PT#M"
# Create new dictionary entry with int value instead, or "Missing" if doesn't exist

ingredients_all = []

for recipe in data:
	ingredients_all.append(recipe["ingredients"])
	try:
		recipe["prepTimeInt"] = recipe["prepTime"][2:-1]
		if "H" in recipe["prepTimeInt"]:
			Hlocation = recipe["prepTimeInt"].find("H")
			hours = int(recipe["prepTimeInt"][:Hlocation])
			minutes = int(recipe["prepTimeInt"][Hlocation+1:])
			recipe["prepTimeInt"] = (hours * 60) + minutes
		if not isinstance(recipe["prepTimeInt"], int):
			recipe["prepTimeInt"] = int(recipe["prepTimeInt"])
	except KeyError:
		recipe["prepTimeInt"] = "Missing"
	except ValueError:
		recipe["prepTimeInt"] = "Missing"
	except TypeError:
		recipe["prepTimeInt"] = "Missing"

# Ask narrowing questions
# Store answers as dictionary values
variables = {}

while True:
	try:
		variables["max_prep_time"] = int(raw_input(
			"How long (in minutes) are you willing to spend preparing the meal? "))
	except ValueError:
		print "Not a number, please try again."
	else:
		break

# Check that requested ingredient exists in recipe data
while True:
	leave_loop = 0
	variables["base_ingredient"] = raw_input(
		"Any thoughts on base ingredient, e.g. potatoes, rice, noodles? (press Enter if not) ").lower()
	for item in ingredients_all:
		if variables["base_ingredient"] in item:
			leave_loop = 1
			break
	if leave_loop == 1:
		break
	print "That ingredient doesn't exist, sorry - could you try again?"
	
while True:
	variables["required_ingredient"] = raw_input(
		"Is there an ingredient that needs using? (press Enter if not) ").lower()
	for item in ingredients_all:
		if variables["required_ingredient"] in item:
			leave_loop = 1
			break
	if leave_loop == 1:
		break
	print "That ingredient doesn't exist, sorry - could you try again?"

# Create new array with only relevant datapoints
# (i.e. those matching the answers provided)
# Then randomly select five from them
# Ask which one is wanted
# Then open the relevant website

# Preparation time
matching_recipes_time = []

for recipe in data:
	if recipe["prepTimeInt"] <= variables["max_prep_time"] and isinstance(recipe["prepTimeInt"], int):
		matching_recipes_time.append(recipe)

matching_recipes_time_ingredients = []

# Ingredients - can do base and key ingredient together
for recipe in matching_recipes_time:
	if (variables["base_ingredient"] in recipe["ingredients"].lower()) and \
		(variables["required_ingredient"] in recipe["ingredients"].lower()):
		matching_recipes_time_ingredients.append(recipe)

# Randomly choose recipes (number set at the top of the file)
chosen_recipes = sample(matching_recipes_time_ingredients, num_choices) 	# Returns array

i = 1

for choice in chosen_recipes:
	print "Recipe %d: " % (i) + choice["name"]
	i += 1

while True:
	try:
		final_choice = int(raw_input("Which number recipe would you like to cook today? "))
	except ValueError:
		print "Sorry, I didn't understand that. Could you try again?"
	else:
		if final_choice >= 1 and final_choice <= num_choices:
			break
		else:
			print "Sorry, that choice seems to be outside the range of recipes."

webbrowser.open(chosen_recipes[final_choice-1]["url"])






