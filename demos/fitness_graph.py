import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
df = pd.read_csv("fitnesslog.csv")
print(df)
fig, ax = plt.subplots()
ax = sns.lineplot(x='Generation', y=' #1 Fitness', data=df, ax = ax, color = '#0398fc')
ax = sns.lineplot(x='Generation', y=' #10 Fitness', data=df, ax = ax, color = '#0398fc')
ax = sns.lineplot(x='Generation', y=' Worst Fitness', data=df, ax = ax, color = 'red')
x = ax.lines[0].get_xydata()[:,0]
y1 = ax.lines[0].get_xydata()[:,1]
y2 = ax.lines[1].get_xydata()[:,1]
ax.fill_between(x, y1, y2, color = 'blue', alpha = 0.3)
plt.show()
