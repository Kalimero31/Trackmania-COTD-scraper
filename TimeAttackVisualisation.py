import numpy as np
import pandas
import matplotlib.pyplot as plt

file = 'COTD_10939.csv'

df = pandas.read_csv('data-COTD/'+file)

times = df['time']
print(len(times))

# Maximum time in seconds to be plotted in here
time_limit = 10

# We keep only the player who are faster than (WR + time_limit)
times = [i for i in times if i< times[0] + time_limit]
print(len(times))

# Calculates the divisions to visualize ( div1, div2, div5k)
divisions_to_visualize = [1, 2] + [5*i for i in range(1, int(int(len(times)/64)/5)+1)]
divisions_times_limit = [times[63+(i-1)*64] for i in divisions_to_visualize]

# Discretizes the time list
interval = 0.1
bins = np.arange(min(times), max(times) + interval, interval)

# Creates a hist
plt.figure(figsize=(15, 10))
plt.hist(times, bins=bins, edgecolor="k", alpha=0.7)

plt.title(file[:-4] + ' - Time attack')
plt.xlabel('Temps (s)')
plt.ylabel('Nombre de joueurs')

# Displays the divisions 
for i, division_time in enumerate(divisions_times_limit):
    if i==0:
        plt.axvline(x=division_time, color='r', linestyle='--', label='division')
    else:
        plt.axvline(x=division_time, color='r', linestyle='--')
    plt.text(division_time, plt.ylim()[1] - 1, ' '+str(divisions_to_visualize[i]), rotation=0, color='r', fontsize=10)

plt.legend(loc='upper right')

# Creates xticks with a regular interval
xtick_interval = 0.5
xticks = np.arange(int(min(times)), int(max(times)) + xtick_interval, xtick_interval)

plt.xticks(xticks)

# Saves the figure
plt.savefig('TimeAttack visualisation/' + str(file[:-4])+ '.png')

# Shows the fig
plt.show()
