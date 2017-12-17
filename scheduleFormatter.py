#!/usr/bin/python
nfl_url = "http://www.espn.com/nfl/schedule"
nba_url = "http://www.espn.com/nba/schedule"
ncaaf_url = "http://www.espn.com/college-football/schedule"

nfl_header = "NFL Schedule"
nba_header = "NBA Schedule"
ncaaf_header = "NCAA Football Schedule"

start_schedule = "[](/start-schedule)"
end_schedule = "[](/end-schedule)"

team_name = {"ATL":"hawks","BKN":"nets","BOS":"celtics","CHA":"hornets","CHI":"bulls","CLE":"cavs","DAL":"mavericks","DEN":"nuggets","DET":"pistons","GS":"warriors","HOU":"rockets","IND":"pacers","LAC":"clippers","LAL":"lakers","MEM":"grizzlies","MIA":"heat","MIL":"bucks","MIN":"timberwolves","NO":"pelicans","NY":"knicks","OKC":"thunder","ORL":"magic","PHI":"sixers","PHX":"suns","POR":"trailblazers","SAC":"kings","SA":"spurs","TOR":"raptors","UTAH":"jazz","WSH":"wizards"}
team_city = {"ATL":"Atlanta","BKN":"Brooklyn","BOS":"Boston","CHA":"Charlotte","CHI":"Chicago","CLE":"Cleveland","DAL":"Dallas","DEN":"Denver","DET":"Detriot","GS":"Golden State","HOU":"Houston","IND":"Indiana","LAC":"LA Clippers","LAL":"LA Lakers","MEM":"Memphis","MIA":"Miami","MIL":"Milwaukee ","MIN":"Minnesota","NO":"New Orleans","NY":"New York","OKC":"Oklahoma City","ORL":"Orlando","PHI":"Philadelphia","PHX":"Pheonix","POR":"Portland","SAC":"Sacramento","SA":"San Antonio","TOR":"Toronto","UTAH":"Utah","WSH":"Washington"}

class ScheduleFormatter():

	sport = "football"

	def createRedditScheduleTable(self,schedule,league_header,schedule_results):

		schedule_table = start_schedule+"\n"

		if league_header == nfl_header:
			schedule_table += "###**[NFL Schedule - "+schedule.week+"]("+nfl_url+")**"
		elif league_header == nba_header:
			self.sport = "basketball"
			schedule_table += "###**[NBA Schedule]("+nba_url+")**"
		elif league_header == ncaaf_header:
			schedule_table += "###**[NCAA Football Schedule - "+schedule.week+"]("+ncaaf_url+")**"

		for res in schedule_results:

			schedule_type = res[0]
			schedule_table += res[1]+"\n\n"

			for game_day in schedule.game_day_order:

				game_day_details = ""
				games = []

				for game in schedule.games[game_day]:
					if schedule_type in game:
						games.append(game)

				if len(games) > 0:

					game_day_details += createRedditScheduleTableHead(schedule_type,self.sport)
					game_day_details += createRedditScheduleTableBody(games,schedule_type,self.sport)

				if game_day_details != "":
					schedule_table += "\n\n*"+game_day+"*\n\n"
					schedule_table += game_day_details

				if self.sport == "basketball":
					break

		return schedule_table+"\n"+end_schedule

	def updateSidebarSchedule(self,sidebar,schedule):

		if start_schedule in sidebar and end_schedule in sidebar:
			sidebar_start_split = sidebar.split(start_schedule)
			sidebar_end_split = sidebar.split(end_schedule)

			if len(sidebar_start_split) == 2 and len(sidebar_end_split) == 2:
				return sidebar_start_split[0] + schedule + sidebar_end_split[1]
			else:
				return sidebar

		else:
			return sidebar
		

def createRedditScheduleTableHead(schedule_type,sport):

	if schedule_type == "time":
		return "Time|Game|Broadcast\n:--|:--:|:--:\n"
	elif schedule_type == "score":
		if sport == "football":
			return "Game|Result|Passing|Rushing|Receiving\n:--|:--:|:--|:--|:--\n"
		else:
			return "Game|Result (Winner,Loser)|Winner High|Loser High\n:--|:--:|:--|:--\n"

def createRedditScheduleTableBody(games,schedule_type,sport):

	schedule = ""

	for game in games:
		if schedule_type == "time":
			schedule += createRedditScheduleGame(game,sport)
		elif schedule_type == "score":
			schedule += createRedditScheduleScore(game,sport)

	return schedule

def createRedditScheduleGame(game,sport):

	if sport == "football":
		return game["time"] + "|" + "[](/" + game["away-abbr"] + ") @ [](/" + game["home-abbr"] + ")|[](/" + game["broadcast"]+ ")\n"
	else:
		return game["time"] + "|" + "[](/" + team_name[game["away-abbr"]] + ") @ [](/" + team_name[game["home-abbr"]] + ")|[](/" + game["broadcast"]+ ")\n"

def createRedditScheduleScore(game,sport):

	if sport == "football":
		return "[](/" + game["away-abbr"] + ") @ [](/" + game["home-abbr"] + ")|" + "[" + game["score"] + "](#s)|[" + game["player-details"][0] + "](#s)|[" + game["player-details"][1] + "](#s)|[" + game["player-details"][2]  + "](#s)\n"
	else:
		return team_city[game["away-abbr"]] +" @ " + team_city[game["home-abbr"]] + "|" + "[" + game["score"] + "](#s)|[" + game["player-details"][0] + "](#s)|[" + game["player-details"][1] +"](#s)\n"

