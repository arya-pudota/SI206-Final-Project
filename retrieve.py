import requests
import sqlite3
import time
import datetime


def get_num_news(teamname:str, date_from:str, date_to:str):
	url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI"

	querystring = {"fromPublishedDate":date_from,"toPublishedDate":date_to,"autoCorrect":"false","pageNumber":"1","pageSize":"10","q":teamname + " Football","safeSearch":"false"}

	headers = {
		'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
		'x-rapidapi-key': "c457108b56msh72bd52d012b3158p1885bfjsnd8a7cbd7ee6e"
		}

	response = requests.request("GET", url, headers=headers, params=querystring).json()
	totalCount = response['totalCount']
	if type(totalCount) == None:
		totalCount = 0
	if totalCount > 250:
		totalCount = 250
	return totalCount

# print (response.json()['totalResults'])

conn = sqlite3.connect('newdb.db')
cur = conn.cursor()

# cur.execute('Drop table Team_Data')
# conn.commit()
# cur.execute('Drop table Team_Name')

cur.execute('''CREATE TABLE IF NOT EXISTS Team_Data (teamrank_id TEXT PRIMARY KEY, year_week TEXT, date TEXT, team_id INTEGER, ranking INTEGER)''')
conn.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS Team_Name (team_id INTEGER PRIMARY KEY, team_name TEXT)''')
conn.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS Team_News (teamrank_id TEXT PRIMARY KEY, team_id INTEGER, num_articles INTEGER)''')
conn.commit()

# date_url = "https://api.collegefootballdata.com/games?year=2019&week=1&seasonType=regular"
# date_response = requests.get(date_url)
# date_str = date_response.json()[0]["start_date"].split("T")[0]
# start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

# for i in range(1,16):
# 	url2 = 'https://api.collegefootballdata.com/rankings?year=2019&week=' + str(i) + '&seasonType=regular'
# 	response2 = requests.get(url2)
# 	rank_data = response2.json()[0]['polls'][0]['ranks']
	
# 	counter = 1
# 	num_teams = cur.execute('SELECT COUNT(*) FROM Team_Name').fetchone()[0]
# 	conn.commit()
# 	#maybe create a teamrank_id (teamname+year+week -> Clemson_2019_1)
# 	#then we can have a table that links teamrank_id to team_name
# 	#the same teamrank_id is also used for our table with the count of number of articles
# 	rank_count = 1
# 	for team_num in range(25):
# 		team_name = rank_data[team_num]['school']

# 		# Ensuring that only 20 items are commited at once
# 		counter+=1
# 		if counter % 20 == 0:
# 			print('Sleeping for 5 seconds during the team rank information retrieval')
# 			time.sleep(1) # TODO: sleep(5)
		
# 		# Checking if the current team already exists in the table
# 		try:
# 			team_id = cur.execute('SELECT team_id FROM Team_Name WHERE team_name=?', (team_name,)).fetchone()[0]
# 		except:
# 			num_teams += 1
# 			cur.execute('INSERT OR IGNORE INTO Team_Name VALUES (?, ?)',(num_teams, team_name,))
# 			team_id = num_teams
		
# 		conn.commit()

# 		cur.execute('INSERT OR IGNORE INTO Team_Data (teamrank_id, year_week, date, team_id, ranking) VALUES (?,?,?,?,?)',(str(team_id)+str(2019)+str(i),str(2019)+str(i), str(start_date.date()), int(team_id), int(rank_count),))
# 		conn.commit()
# 		rank_count+=1
# 		# print(cur.execute('select * from Team_Data').fetchall())
# 	start_date += datetime.timedelta(days=7)

#we want team_id and date
return_id_names = cur.execute('SELECT Team_Data.date, Team_Data.team_id, Team_Name.team_name, Team_Data.teamrank_id FROM Team_Data INNER JOIN Team_Name ON Team_Data.team_id == Team_Name.team_id').fetchall()
counter = 1
for team in return_id_names:
	date_str = team[0]
	start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
	end_date = start_date + datetime.timedelta(days=7)
	number_article = get_num_news(team[2], str(start_date.date()), str(end_date.date()))
	cur.execute('INSERT OR IGNORE INTO Team_News (teamrank_id, team_id, num_articles) VALUES (?,?,?)', (str(team[3]), team[1], number_article))
	conn.commit()
	
	counter += 1
	if counter % 20 == 0:
		print('Sleeping for 5 seconds during the news retrieval period')
		time.sleep(1)

#finding the start date

