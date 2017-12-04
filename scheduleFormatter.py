#!/usr/bin/python
nfl_url = "http://www.espn.com/nfl/schedule"
nba_url = "http://www.espn.com/nba/schedule"
ncaaf_url = "http://www.espn.com/college-football/schedule"

nfl_header = "NFL Schedule"
nba_header = "NBA Schedule"
ncaaf_header = "NCAA Football Schedule"

class ScheduleFormatter():

	sport = "football"

	def createRedditScheduleTable(self,schedule,league_header,schedule_results):

		schedule_table = ""

		if league_header == nfl_header:
			schedule_table += "[NFL Schedule - "+schedule.week+"]("+nfl_url+")"
		elif league_header == nba_header:
			self.sport = "basketball"
			schedule_table += "[NBA Schedule]("+nba_url+")"
		elif league_header == ncaaf_header:
			schedule_table += "[NCAA Football Schedule - "+schedule.week+"]("+ncaaf_url+")"

		schedule_table = ""

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

		return schedule_table

def createRedditScheduleTableHead(schedule_type,sport):

	if schedule_type == "time":
		return "Time|Game|Broadcast\n:--|:--:|:--:\n"
	elif schedule_type == "score":
		if sport == "football":
			return "Result|Game|Passing|Rushing|Receiving\n:--|:--:|:--|:--|:--\n"
		else:
			return "Result|Game|Winner High|Loser High\n:--|:--:|:--|:--\n"

def createRedditScheduleTableBody(games,schedule_type,sport):

	schedule = ""

	for game in games:
		if schedule_type == "time":
			schedule += createRedditScheduleGame(game)
		elif schedule_type == "score":
			schedule += createRedditScheduleScore(game,sport)

	return schedule

def createRedditScheduleGame(game):

	return game["time"] + "|" + "[](/" + game["away-abbr"] + ") @ [](/" + game["home-abbr"] + ")|[](/" + game["broadcast"]+ ")\n"

def createRedditScheduleScore(game,sport):

	if sport == "football":
		return "[" + game["score"] + "](#s)" + "|" + "[](/" + game["away-abbr"] + ") @ [](/" + game["home-abbr"] + ")|"+ game["player-details"][0] + "|" + game["player-details"][1] + "|" + game["player-details"][2]  + "\n"
	else:
		return "[" + game["score"] + "](#s)" + "|" + "[](/" + game["away-abbr"] + ") @ [](/" + game["home-abbr"] + ")|"+ game["player-details"][0] + "|" + game["player-details"][1] +"\n"

