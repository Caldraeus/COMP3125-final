import pandas as pd # For dataframes and etc
from datetime import datetime as dt # For date/time comprehension
import matplotlib.pyplot as plt # For images of data plots
import numpy as np
import seaborn as sn # For heatmap and etc
import sys

pd.set_option('display.max_columns', None)
plt.rcParams["figure.figsize"] = (13, 7)

# Import datasheet.
try:
    raw_data = pd.read_csv("Data/over_one_mil_chars.csv", index_col=0)
except:
    print("Please download the .csv file and place it into the data directory. You can find the data here: https://www.kaggle.com/datasets/maximebonnin/dnd-characters-test")
    sys.exit()

print("Data Loaded.")

# First we need to rename the "stat" columns to be a little more sensical...
index_names = {
    "stats_1": "strength",
    "stats_2": "dexterity",
    "stats_3": "constitution",
    "stats_4": "intelligence",
    "stats_5": "wisdom",
    "stats_6": "charisma",
}

raw_data.rename(columns=index_names, inplace=True)

# Next, I got rid of the columns I would not be needing.
# raw_data = raw_data.drop(columns=["notes_len"]).dropna()
# Just kidding! Upon further investigation, some characters have nothing in their inventory yet - which makes sense! So we need to keep those here.

# Cool! Now, let's also clean up some unrealistic characters.
# D&D Characters can only be levels 1 to 20, so first...
raw_data = raw_data[(raw_data['total_level'] <= 20)] 

# Next, I am going to remove people with 0 or negative gold, and people with over 1 million gold - I will explain why in my readme.md
realistic_gold_data = raw_data[(raw_data['gold'] > 0) & (raw_data['gold'] < 750000)] 

# Alright, good. Now, lets order by total level, and while we're at it, remove all columns but the ones we need.
# This will be useful for our grouby function later on.
gold_data = realistic_gold_data.sort_values(by="total_level", ascending=True)
gold_data = realistic_gold_data[['total_level','gold']]

# We want to get the average wealth per level.
grouper = gold_data.groupby(["total_level"], as_index=False)
data = grouper.sum()
data.columns = ("Level", "Total Gold")
data["Avg Gold"] = grouper.mean()["gold"]

print(data)

wealth_frame = pd.DataFrame(data, columns=['Level', 'Total Gold', 'Avg Gold'])
print(wealth_frame)

wealth_frame.plot(x='Level', y='Avg Gold', title='Avg Gold Per Level').set_xticks(np.arange(1,21,1))
plt.show()

# Next, lets calculate the most popular D&D class.
# We first remove the characters with an invalid class.
class_data = raw_data[~(raw_data['class_starting'] == 'Blood Hunter (archived)') & ~(raw_data['class_starting'] == 'Artificer') & ~(raw_data['class_starting'] == 'Blood Hunter') & ~(raw_data['class_starting'] == 'Artificer (UA)')]
class_data = class_data['class_starting'].value_counts()

class_data.plot.bar(title="# of Total Character Classes")
print(class_data)
plt.show()

# Now, what about the most popular class/race combination?
# Get rid of any race that doesn't have more than 200 entries - these are likely homemade races that aren't in any sourcebooks.
print("-"*30)

real_races = pd.DataFrame(raw_data["race"].value_counts()) # Gets us all the races and their occurences
real = real_races[real_races["race"] >= 200].index # We're going to ignore anything with less than 200 occurences, as these could be made up races, etc

# I am once again getting rid of the invalid classes for this.
class_race = raw_data[~(raw_data['class_starting'] == 'Blood Hunter (archived)') & ~(raw_data['class_starting'] == 'Artificer') & ~(raw_data['class_starting'] == 'Blood Hunter') & ~(raw_data['class_starting'] == 'Artificer (UA)')]
class_race = class_race[["race", "class_starting"]].query("race in @real") # Query to check if theyre in our value counts

class_race = class_race.pivot_table(index='race', columns=['class_starting'], aggfunc=len, fill_value=0)
# Fill value will make any non-existing combinations in our data just zero instead of null.

sn.heatmap(class_race, cmap="Spectral")
plt.show()

# Next, lets determine the most popular items.
# As we learned earlier, some people had empty inventories. This time, we can safely dropna() on it since we won't be needing them

inv = raw_data["inventory"].dropna()

# Each item is in a list, seperated by a / character. We need to fix this.
# Originally did this with for loops, which took way to long, and ended up with a crash.

# Instead, lets try list comprehensions?
# First, lets do something like "x in y for x in z" sorta
sublists = [items.split("/") for items in list(inv)]
# Basically: For each list of items inside list(inv), split those items into a list (splitting on / character)

# Next, for each items list in sublists, add each item into a normal array
fin_arr = [item for items in sublists for item in items]
# Basically: Add the individual item to fin_arr for each list of items in the sublists for each array inside sublists

inv_df = pd.DataFrame(fin_arr).value_counts(ascending=False)

print(inv_df.iloc[:15])

inv_df.iloc[:15].plot.bar(color = '#3EB489')
plt.xticks(rotation=45, ha='right')
plt.show()

# Finally, compare most popular feat for each class, using another heatmap.
print("-"*30)

# We want something like "Fighter | Grappler"
classfeats = raw_data[["class_starting", "feats"]].dropna()
classfeats = classfeats.to_dict(orient='records')

# Clean up the sublists
class_lists = [{info["class_starting"]:info["feats"].split("/")} for info in classfeats]

# Combine all dicts in this list.
# NOTE: Very, VERY slow code. Not sure how to optimise.
combo_dict = {}

# Originally, I was calling .values and .keys, but that's too slow. This code is a lot faster!
for entry in class_lists:
    key = list(entry.items())[0][0]
    values = list(entry.items())[0][1]
    combo_dict[key] = combo_dict.get(key, [])
    combo_dict[key].extend(values)

final_frame = pd.DataFrame()
final_frame = pd.concat({k: pd.Series(v) for k, v in combo_dict.items()})

# Alright, we now have a multi-indexed frame with feats and classes together.
# Lets start by finding and plotting the most popular feats!

final_frame.value_counts(ascending=False).iloc[:15].plot.bar(color = '#FFD700')
plt.xticks(rotation=45, ha='right')
plt.show()

# Next, lets try determining the most popular feat per class.
# Convert the series to a dataframe with a default index
final_frame = final_frame.reset_index()

# Set the columns 0 and 1 as the multi-index
final_frame = final_frame.set_index(['level_0', 'level_1'])

final_frame.rename(columns = {list(final_frame)[0]: 'feat'}, inplace = True)

# Using the same method for races, we're going to filter out reall low occuring feats
real_feats = pd.DataFrame(final_frame["feat"].value_counts()) # Gets us all the feats and their occurences
real = real_feats[real_feats["feat"] >= 200].index # We're going to ignore anything with less than 200 occurences, as these could be made up races, etc

# I am once again getting rid of the invalid classes for this.
final_frame = final_frame.query("feat in @real") # Query to check if theyre in our value counts

final_frame = final_frame.pivot_table(index = 'level_0', columns=['feat'], aggfunc=len, fill_value=0)

sn.heatmap(final_frame, xticklabels=True, yticklabels=True)
plt.show()