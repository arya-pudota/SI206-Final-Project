import sqlite3
import datetime
import matplotlib.pyplot as plt
import numpy as np

#viz 1: rank teams according to number of news articles
#viz 2: 1 -> 58

conn = sqlite3.connect('newdb.db')
cur = conn.cursor()
#Visualization 1
def create_viz_1():
	cur.execute('''SELECT Team_Name.team_name, SUM(Team_News.num_articles) AS 'Articles' FROM Team_Name 
					INNER JOIN Team_News ON Team_News.team_id == Team_Name.team_id 
					GROUP BY Team_News.team_id 
					ORDER BY Articles DESC''')
	conn.commit()
	data = cur.fetchall()
	x_axis = []
	y_axis = []
	file1 = open(r"viz_1.txt", 'w')
	for i in range(15):
		x_axis.append(data[i][0])
		y_axis.append(data[i][1])
		file1.write(data[i][0] + "\t" + str(data[i][1]) + '\n')
	file1.close()
	f1 = plt.figure()
	plt.bar(x_axis, y_axis)
	plt.title('Team vs. Total Popularity')
	plt.xlabel('Teams')
	plt.ylabel('Number of articles published')
	plt.savefig('Team_vs_Popularity.png')


def create_viz_2():
	cur.execute('''select year_week, SUM(Team_News.num_articles) from Team_Data INNER JOIN Team_News ON Team_Data.teamrank_id == Team_News.teamrank_id GROUP by year_week ORDER by year_week''')
	conn.commit()
	data = cur.fetchall()
	x_axis = []
	y_axis = []
	for i in range(15):
		x_axis.append(int(data[i][0][4:]))
		y_axis.append(data[i][1])

	x_axis = np.array(x_axis)
	y_axis = np.array(y_axis)

	new_x_axis = np.argsort(x_axis)
	x_axis = x_axis[new_x_axis]
	y_axis = y_axis[new_x_axis]

	file2 = open(r'viz_2.txt', 'w')

	for i in range(15):
		file2.write(str(x_axis[i]) + '\t' + str(y_axis[i]) + '\n')
	file2.close()

	f2 = plt.figure(2)
	plt.plot(x_axis, y_axis)
	plt.title('Week vs. Popularity')
	plt.xlabel('Week Number')
	plt.ylabel('Number of articles published')
	plt.savefig('Week_vs_Popularity.png')


create_viz_1()
create_viz_2()