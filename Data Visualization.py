import PythonPandasPractice_1 as p1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd

# Create Features / Target Variables (Make Flashcards)
#dfurls = p1.info.clean_data()
dffh1 = p1.fighthistory1
dffh2 = p1.fighthistory2

sns.set_theme(style="whitegrid")

#convert all cells to int datatype from string
for i in range(len(dffh1)):
    dffh1.loc[i, "Str_fighter"] = int(dffh1.loc[i, "Str_fighter"])
    dffh1.loc[i,"Str_opponent"] = int(dffh1.loc[i,"Str_opponent"])

strikes = dffh1.set_index('Event').plot(kind='bar', y=["Str_fighter", "Str_opponent"], stacked=True, color=['#1f77b4', '#d62728'])

top_bar = mpatches.Patch(color='#1f77b4', label='Fighter')
bottom_bar = mpatches.Patch(color='#d62728', label='Opponent')
plt.legend(handles=[top_bar, bottom_bar])
plt.setp(strikes.get_xticklabels(), rotation=45, ha='right')
plt.show()
plt.close()


opponent_stats = p1.F2_info.find_fighter()
opponent_stance = opponent_stats['Stance']
#Create function to find fighters who fighter1 has fought with the same stance
def fights_against_stance(stance):
    for i in range(len(dffh1)):
        fighter = dffh1.loc["Opponent", i]
        fighter_link = 