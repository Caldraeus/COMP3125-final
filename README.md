# Data Science Individual Projcet

## Introduction
For my individual project, I found a dataset that has to do with one of my favorite hobbies - Dungeons & Dragons! This dataset had information about characters such as their inventories, feats, levels, and more. I wanted to know what people liked - what classes were popular? What items were popular? Which race was best for what class? What feats were used the most? How much gold do people have? These were all questions I had going into this project.

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
Now that we have our methods, let's check out our results, starting with average gold.
![gold](https://github.com/Caldraeus/dndbeyond-analysis/blob/master/images/avg_gold.png?raw=true)
Here, we see a pretty interesting spread of data. Characters start with more gold at level one than later levels, then dip down, then the gold rises (with a few dips along the way) until we hit level 16, where it goes down. Then, from level 18 to level 19, there's a massive jump, until we then drop a lot at level 20. Quite the datapoint rollercoaster, for something I imagined would be pretty linear! I have a few theories as to why this is, which we will talk about in the discussion section.

![class_feat](https://github.com/Caldraeus/dndbeyond-analysis/blob/master/images/class_feat.png?raw=true)
Here were the results for our most popular feat by class. It's a little bit condensed on the x-axis, but I did as much as I could to make it readable.

Here, we can see that grappler is the most popular feat overall - in fact, it's mostly popular with fighters, which makes sense - fighters can make the most out of this feat!

Additionally, you can see that "sharpshooter" is popular amongst Rangers. Ranger is traditionally the "ranged" class, and sharpshooter is a feat that supports a ranged playstyle, so it makes sense. I will expand more on this in the following section as well.

![feats](https://github.com/Caldraeus/dndbeyond-analysis/blob/master/images/feat_popularity.png?raw=true)
Here's a second feat visualization showing the most popular feats amongst all classes. Note the abnormally high spike in Grappler - there is a reason for this beyond it just being a popular feat.

![class_race](https://github.com/Caldraeus/dndbeyond-analysis/blob/master/images/class_race.png?raw=true)
Here, we can see the most popular races among classes! The popular D&D joke about "Human Fighter" being the most overused class/race combo isn't just a joke - it appears it's grounded in reality. Additionally, we see that elves are used a lot for rangers, which I found interesting. 

![class_pop](https://github.com/Caldraeus/dndbeyond-analysis/blob/master/images/total_classes.png?raw=true)
Here, we can see the most popular D&D classes overall. We can see clearly that Fighter is the most popular, while Druid is the least popular. Cleric seems to fall directly in the middle, and to my surprise, Warlock wasn't as popular as I had predicted.

![items](https://github.com/Caldraeus/dndbeyond-analysis/blob/master/images/item_popularity.png?raw=true)
Finally, we can see the most popular items among inventories of characters. These results weren't too unexpected, for the most part. It makes perfect sense that a backpack is the most common item, considering you need it to carry your other items. This is then followed by dagger and rations (1 day). These also made sense, since a lot of people start with a dagger as a backup weapon, and everyone carries multiple instances of 1-day rations in order to eat!
## Discussion
Now that we've reviewed our data visualizations, let's talk about what the implications of this data are.

First, let's consider what we saw in the average gold per level chart. There are a few important things of note;
1. Level 1 characters had more gold than level 2 and 3 characters.
2. From levels 16 to 18, there is a noticeable dip in gold.
3. Gold peaks at level 19, then dips at level 20.

Now, I have a few ideas as to why these trends happen. 
1. Level 1 characters are fresh - they have not had time to spend their gold yet, unlike level 2 and 3 characters, who have likely spent money on healing potions or other items.
2. Level 16 through 18 characters likely buy better items, or spend all their money, as a lot of campaigns end around this level - meaning they spend the rest of their money before the game ends.
3. Level 20 characters are incredibly powerful - it is likely that, at this point, money has no worth to them, so they just buy whatever. It is also likely that campaigns end at level 20 as well, meaning they also spend the rest of their money.

These are just a few of my initial thoughts as to why there might be these trends in the gold per-level chart. Next, let's check out the most popular feats per class.
___
Here, we've got a large heatmap comparing feat popularity amongst classes, as well as a bar plot of the most popular feats overall. Grappler is the most used overall, primarily for fighters, which makes sense. On D&D Beyond, the website this data is stripped from, free accounts can only use one feat - the grappler feat. Therefore, the "popularity" of the grappler feat is skewed by the limitations the website has.

Interestingly, svirfneblin magic is one of the most used feats for characters in this dataset, which is very interesting. Svirfneblin magic (SM) isn't a very common feat - it's restricted to a specific race, so I'm not entirely sure why it's so popular on D&D beyond. Perhaps there are a lot of characters that took SM as a test, or maybe this data was collected when SM first came out, so more people had taken it to use it.

Finally, the usefulness of this heatmap comes when determining which feat to take depending on what class you're playing. For example, let's imagine you're playing a Ranger. When we look at the heatmap, we see that the most popular feat (ignoring Grappler) is Sharpshooter! This makes sense, as sharpshooter is a feat that works very well with Ranger's playstyle. 

This heatmap could also be useful for the designers of D&D, Wizards of The Coast (WotC), to determine which feats might be good or bad in design. If a feat has little to no use, that means it's either bad, unfun or just uninteresting. However, if a feat is used a lot (such as grappler, sharpshooter, war caster), that means that it's well designed or powerful, or in some cases, too powerful. These metrics can be useful for WotC to determine how to design future feats.
___
Next, we can take a look at our second heatmap, displaying the most popular race/class combination. This, like the feat/class heatmap, can be useful for many of the same reasons. Let's say, for example, you're playing a Druid - which race do you play, if you're new to D&D, and want to do something that's known to be good? Well, when you take a look at our heatmap, you can see that Elf seems to be the most used race for Druid! 

Another thing that was interesting here, is that Human/Fighter is the most common race/class combination. As I have mentioned before, there is a very common joke in the D&D community about Human Fighters being the most common and most boring or generic D&D characters out there. It's interesting to see that this joke is grounded in reality, as the Human/Fighter combo shows up more than any other combination in the game.

Like the previous heatmap, this is a good metric for WotC game designers to determine what is popular and well designed, and unpopular or less designed. For example, the heatmap shows that Yuan-ti Pureblood is barely used, no matter the class. This gives the WotC game designers a reason to go back and determine why this is - perhaps it's boring, or just not a powerful choice for players.
___
Next, we have a small bar graph displaying the popularity of classes overall. Knowing what we know about the Human/Fighter popularity, it comes as no surprise that Fighter is the most popular class. It also is no surprise that most of the spellcaster classes (Warlock, Wizard, Sorcerer, Cleric, Druid) are a little bit lower than the martial classes (Ranger, Fighter, Paladin, Barbarian).* Spellcaster-centerered classes can be a little bit more difficult for new players, as they have complicated mechanics and a lot to keep track of. Additionally, at earlier levels, spellcasters can feel weaker or less fun than the martial classes, which could play a factor in their popularity.

This information can be useful for new players, who are unsure of which class to play. If they want to go with something more popular, easier to understand, and powerful, they can take a look at the popularity chart and go with something near the top, such as Fighter.

One thing about this data that stood out to me was how low Barbarian was on the popularity list. Barbarian has always been one of the classes I had seen a lot of in my real-life games, so I had expected it to be higher on the list - it's easy to play, fun, and powerful. But the data showed that it wasn't as popular as I thought it to be.

###### *While these classes can also have spellcasting at higher levels, they are less spellcasting heavy overall.
___
Finally, we have the popularity of inventory items. This data is not unexpected. When you start off in D&D, you are asked to choose a “pack”. These packs have varied items, but almost all of them come with a backpack, a mess kit, a torch, a bedroll, clothes (common), and 50 feet of rope. All of these items make appearances in our top 15 items, which makes perfect sense.

Something that’s interesting here as well as the popularity of weapons. In D&D, you have a lot of choices for what weapons to take. According to the table, it appears Daggers, Shields, and Short Swords are the most commonly used, which is an interesting trend. 

This data can be useful for players trying to figure out what items to take or buy when they go to a shop. I never considered the usefulness of having a spare dagger in D&D - maybe I’ll give it a shot next time I play!

## Summary
In summary, these are the most important things to note from this data.
- Human Fighters are the most popular class combination, followed by Elven Ranger and Tiefling Warlock
- Grappler is a popular feat on D&D beyond, followed by War Caster, and then SM
- Gold peaks before the 20th level and 16th level, so if you know your campaign is ending soon and you're near those levels, you can spend it knowing you won't need to worry about having less at the next levels/afterward.
- The most popular class is fighter, and the least popular class is druid.
- Most characters carry a spare dagger, shield, or crowbar

This information is good for new players trying to make a well-rounded character, or perhaps for more veteran players wanting to work outside the box and create something more unique, like a Triton Monk with the Healer feat.

Additionally, WotC game designers can review this information to help create new content or balance existing content for the betterment of game health and enjoyability.

This concludes my analysis of the D&D Beyond dataset! Thank you for reading.
## References
https://www.kaggle.com/datasets/maximebonnin/dnd-characters-test/code?resource=download

https://www.dndbeyond.com/forums/dungeons-dragons-discussion/dungeon-masters-only/79378-character-wealth-gold-by-level#c11