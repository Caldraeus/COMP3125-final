# Data Science Individual Projcet

## Introduction
For my individual project, I found a dataset that has to do with one of my favorite hobbies - Dungeons & Dragons! This dataset had information about characters such as their inventories, feats, levels, and more.

## Selection of Data
For my data, I found a very in-depth dataset on Kaggle using information from the popular D&D character creation website, D&D Beyond. The data set had many columns:

1. char_id
    - The character's "ID" for D&D Beyond's purposes
2. name
    - This was the date that the transaction occurred
3. base_hp
    - This was the character's base hitpoints, without any modifiers
4. stats_1
    - This represented that character's *Strength* score.
5. stats_2
    - This represented that character's *Dexterity* score.
6. stats_3
    - This represented that character's *Constitution* score.
7. stats_4
    - This represented that character's *Intelligence* score.
8. stats_5
    - This represented that character's *Wisdom* score.
9. stats_6
    - This represented that character's *Charisma* score.
10. background
    - This had information about the chosen character's "background"
11. race
    - This included information about the character's race (elf, human, orc, etc)
12. class_starting
    - Represented the character's initial class, before multiclassing levels.
13. class_starting_level
    - Represented the character's level in the starting class
14. subclass_starting
    - Represented the character's starting class's subclass. For example, someone's starting class was Rogue, and their starting class subclass was Swashbuckler.
15. class_other
    - Represented any other multiclassing character class the character could have.
16. subclass_other
    - Represented the subclass of their secondary classes, if applicable. 
17. total_levels
    - Represents the total overall level of a character.
18. feats
    - Had a list with items seperated by a `/` character of the character's feats.
19. inventory
    - Had the character's inventory, with items seperated by a `/` character again.
20. date_modifier
    - Had information on the last time the character was edited on D&D Beyond's website.
21. notes_len
    - The length of the character notes. 
22. gold
    - How much gold the character had.

## Methods
Upon first viewing this file, I noticed there were a lot of incomplete characters - that is, characters with impossible health values (zero or below), no stats, or otherwise incomplete data. I also noticed another thing - some characters were likely built as a "test" character - they had a large amount of magic items, millions of gold (which, while not impossible, is largely considered an unrealistic feat within D&D), or some other obscenely powerful or surplus of something or other. 

When I first began, I had absentmindedly run a `.dropna()` call, thinking it would clean out any incomplete characters. However, as I continued working with the now (incorrectly) cleaned data, I noticed that there were no level 1 characters. With over 2 million character entries in this dataset, there was absolutely no way that there wasn't, at the very least, one level 1 character. 

So, I had to take a step back and manually check out the .csv file for a bit. As it turns out, when I called `.dropna()`, I had, without thinking, gotten rid of any character with no gold, no inventory, and no subclass - all things that are, as it turns out, very consistent with level 1 characters.

So, how do we solve the issue of players with obscenely high amounts of gold? Well, I ended up going with a simple solution: remove all characters with over 750,000 gold.

There is a good reaon for doing this, so let me explain. D&D characters oftentimes never accumulate one million gold *alone*. A D&D characater is usually in a party of 3-5 other D&D characters, where accumulating one million gold as a party is a feat alone. That said, how do we decide how much gold is "unrealistic" for one D&D character to have? We would need some sort of reference for what kind of gold is normal for a character to have. Thankfully, there are several sourcebooks for Dungeons & Dragons 5e that have information on wealth, of which other people have done a lot of work with to calculate average gold per level for. For this project's sake, we will use work done by user "Ajexton". According to Ajexton, they calculated the average gold per level found in the table below.

| Character Level   | Wealth Upon Reaching Level (in Gold Pieces) |
| :---------------: | :-----------------------------------------: |
| 1                 | Starting Gear*                              |
| 2                 | 94g                                         |
| 3                 | 188g                                        |
| 4                 | 376g                                        |
| 5                 | 658g                                        | 
| 6                 | 2930g                                       |
| 7                 | 5404g                                       |
| 8                 | 8610g                                       |
| 9                 | 12,019g                                     |
| 10                | 16,563g                                     |
| 11                | 21,108g                                     |
| 12                | 30,161g                                     |
| 13                | 39,214g                                     |
| 14                | 57,320g                                     |
| 15                | 75,427g                                     |
| 16                | 102,586g                                    |
| 17                | 129,745g                                    |
| 18                | 214,204g                                    |
| 19                | 383,123g                                    |
| 20                | 552,042g                                    |
###### **starting gear is not included in any entry after level 1*

Additionally, it is worth noting that the author of this table said the following:

> *"I took an average (Using the DMG and Xanathar)** *and rounded up so the numbers were easier to remember. But honestly the amounts are close enough that you could use either and it won’t break your game. These aren’t meant to be exact amounts anyways, it’s just a 'ball-park' number for DM’s to use as a guide."*
###### **these are both Dungeons & Dragons official sourcebooks.*

The important part of this is how they said that these aren't exact amounts, just ball-park numbers. Dungeons & Dragons is a very, very variable game - no two times playing it will be the same. Unlike a videogame, which is set in stone with rules, code and solid systems, D&D's rules are mostly "guidelines" on how to run the game - if someone wanted to run a game where everyone started with one million gold, they could! So, for the sake of this project, we are going to use characters that fall within the bound set by the core rule books of D&D, which includes the wealth table above.

Moving on, we can see from this table that the average wealth of a level 20 character is 552,042 gold. This is just the average and I have been in games where a player character has accumulated a lot more gold than normal, so I decided that anyone over 750,000 gold would be considered "unrealistic".

Now that we've cleaned out characters labeled as "unrealistic", we can finally go through and calculate our averages. Originally, I was doing this like so:

```python
for i in range(20):
    temp = test[(test["total_level"] == i+1)]    
    total_g = temp["gold"].sum()
    mean_g = temp["gold"].mean()
    # print(f"Total Gold For Level {i+1}: {total_g} (avg of {mean_g})")
    data.append([i+1, total_g, mean_g])
```
But, I remembered Pandas has a `.groupby()` function! So, we were able to cut down this code to be the following.
```python
grouper = test.groupby(["total_level"], as_index=False)
data = grouper.sum()
data.columns = ("Level", "Total Gold")
data["Avg Gold"] = grouper.mean()["gold"]
```
After switching to using this `groupby()` call, I did have to go back and cut off all columns that weren't what we needed, but that wasn't too difficult.

Interestingly, I ran this code again when setting the maximum gold cutoff to 1750000, and found that the data doesn't actually change by much... which means I was likely correct about there being a lot of test characters in the dataset, where the creator gave themselves an obscenely high amount of gold for testing purposes. 
___
Next, I wanted to do a simple calculation of what the most popular D&D classes were. I have always been curious about this metric, and I had a hypothesis based on my own experiences playing D&D - I figured the most popular class would either be Fighter or Warlock and that the least popular would be Druid. Why? Well, Fighter is one of the most versatile classes in D&D, and Warlocks have very powerful character abilities. On the other hand, I have just seen less druids than any other class, so I just guessed it might be the least popular. For this part, we don't care if the characters have an "unrealistic" amount of gold, items, or etc - all we care about is what class they began as - even testing characters will play a part in class popularity, as it shows what people are considering playing in the future.

Before we continue to calculating the most popular classes, we had to first do a little bit of data munging. There were a few classes within the dataset that wouldn't be accurate, namely **Artificer** and **Blood Hunter**. I was only curious in the core D&D classes - both Artificer and Bloodhunter came from an expansion to the main rules, so I filtered the data to remove these classes before determining class popularity.

To determine the popularity of classes, I did the following.

```python
class_data = raw_data[~(raw_data['class_starting'] == 'Blood Hunter (archived)') & ~(raw_data['class_starting'] == 'Artificer') & ~(raw_data['class_starting'] == 'Blood Hunter') & ~(raw_data['class_starting'] == 'Artificer (UA)')]

class_data = class_data['class_starting'].value_counts()
```
First, we I use an obscenely long line of code *(sorry Pylint!)* to remove all of the invalid classes, then use a simple `.value_counts()` to count the occurences of each class. 
___
Next, I wanted to figure out the most popular species (also called a race) / class combo in D&D. One of the most popular D&D jokes is how a Human Fighter is the most common, boring, and overused D&D character, so I wanted to discover if this was a true fact!

To do so, I spent some time researching and found out the best way to do this would be a heatmap. I was originally having some issue converting to a heatmap, and discovered on a [StackOverflow](https://stackoverflow.com/questions/37790429/seaborn-heatmap-using-pandas-dataframe) page that I would have to first convert it to a `pivot_table`. I wasn't sure why, but as it turns out, a heatmap needs a 2D input - that's why we need to use pivot table. I wasn't quite sure on how to do so, but after digging around on the internet, I eventually did the following.
```python
class_race = class_race.pivot_table(index='race', columns=['class_starting'], aggfunc=len, fill_value=0)
```
I figured out I had to use `len` as my aggfunc here to determine the total counts, which made sense - credit to [this post](https://stackoverflow.com/questions/22412033/python-pandas-pivot-table-count-frequency-in-one-column) for explaining to my why.

I had also filtered out all races with less than 200 occurences in the csv file - there were a lot of races that were either homebrew or new, with minimal usage, which would gum up our final result.
___
Next, I wanted to figure out the most popular items that the characters had. This part was deceivingly simple - I thought I could just use some for loops, go through each list of items, split them into sublists (they are stored as strings, using a `/` character to separate each item) and then add those all to one big list. Unfortunately, this timed out when I did this, so instead, I used some list comprehensions, one of my favourite aspects of python.
```python
inv = raw_data["inventory"].dropna()
sublists = [items.split("/") for items in list(inv)]
fin_arr = [item for items in sublists for item in items]
```
This is a little weird, but essentially, we start by splitting each text-list in the original raw data into a sublist containing each item, adding that to our `sublists` variable. This leaves us with a 2D array of a bunch of lists of items, so we then go through each of these, add the `item` to fin_arr, for each item in each list of items in the sublists array. A little weird in code, but it works.

From there, we do some value counts, and graph it.
```python
inv_df = pd.DataFrame(fin_arr).value_counts(ascending=False)

print(inv_df.iloc[:15])

inv_df.iloc[:15].plot.bar(color = '#3EB489')
plt.xticks(rotation=45, ha='right')
plt.show()
```

Nice! That gives us the 15 most popular items. I theorized that the #1 item would be 50 feet of rope (almost every character in D&D starts off with this in their inventory, and often times it is never used), and I wasn't too far off! 
___
Finally, I wanted to calculate the most popular feat amongst each class. This is done in a similar way to how we calculated the most popular race amongst each class, but since feats are stored in a string-list format, like inventory, there were a few extra steps.

First, I ran the following code.
```python
classfeats = raw_data[["class_starting", "feats"]].dropna()
classfeats = classfeats.to_dict(orient='records')

# Clean up the sublists
class_lists = [{info["class_starting"]:info["feats"].split("/")} for info in classfeats]
```
This constructed a list of dictionaries with lists as their value. This was hard to work with, so I needed a way to combine these all into one big dictionary with class : feats.

First, I tried this code:
```python
for entry in class_lists: 
	try: combo_dict[list(entry.keys())[0]] = combo_dict[list(entry.keys())[0]] + list(entry.values())[0] 
	except KeyError: 
		combo_dict[list(entry.keys())[0]] = list(entry.values())[0] 

final_frame = pd.concat({k: pd.Series(v) for k, v in combo_dict.items()})
```

However, this was insanely slow, so we have to find a way to do this a bit better.

To optimize the code, we can avoid using the keys() and values() methods of the dict object, as they require creating two new lists each time they are called.

Since the values in the `combo_dict` dictionary are lists, we can use the `extend()` method to add the new values to the existing values more efficiently than using the + operator. This can be done like this:

```python
for entry in class_lists:
    key = list(entry.items())[0][0]
    value = list(entry.items())[0][1]
    combo_dict[key] = combo_dict.get(key, [])
    combo_dict[key].extend(value)
```
In this updated version of the code, the combo_dict[key] value is initialized to an empty list if the key does not exist, and then the extend() method is used to add the new values to the existing list. This avoids the need to use the update() method and makes the code more efficient for concatenating lists.

After this, we convert this to a dataframe, and then map it as we did with class to race, using seaborn and its heatmap function. 

Now that we're done talking about our methods and how we're getting our information, let's check out the results.

## Results

## Discussion

## Summary

## References
https://www.kaggle.com/datasets/maximebonnin/dnd-characters-test/code?resource=download

https://www.dndbeyond.com/forums/dungeons-dragons-discussion/dungeon-masters-only/79378-character-wealth-gold-by-level#c11