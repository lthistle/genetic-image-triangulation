import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
df = pd.read_csv("results/log.csv")
print(df)
fig, ax = plt.subplots()
ax = sns.lineplot(x='generation', y='best_fitness', data=df, ax = ax)
ax = sns.lineplot(x='generation', y='10_fitness', data=df, ax = ax, color = '#0398fc')
ax = sns.lineplot(x='generation', y='worst_fitness', data=df, ax = ax, color = 'red')
plt.legend(labels=['Best fitness', '90th percentile', 'Worst fitness'])
x = ax.lines[0].get_xydata()[:,0]
y1 = ax.lines[0].get_xydata()[:,1]
y2 = ax.lines[1].get_xydata()[:,1]
ax.fill_between(x, y1, y2, color = 'blue', alpha = 0.3)
ax.set_title("Population Fitness over Time")
plt.xlabel("Generation #")
plt.ylabel("Fitness")
plt.show()
