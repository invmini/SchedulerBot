#!/usr/bin/python
from datetime import datetime, tzinfo, timedelta

nfl_url = "http://www.espn.com/nfl/schedule"
nba_url = "http://www.espn.com/nba/schedule"
ncaaf_url = "http://www.espn.com/college-football/schedule"

nfl_header = "NFL Schedule"
nba_header = "NBA Schedule"
ncaaf_header = "NCAA Football Schedule"

from HTMLParser import HTMLParser

class ESPNParser(HTMLParser):

	games = {}
	game_day_order = []
	week = ""

	in_schedule = False

	grab_week = False
	grab_games = False
	grab_game_day = False

	in_game = False
	grab_away_team = False
	grab_home_team = False
	grab_abbr = False
	grab_network = False
	grab_score = False
	grab_player = False
	grab_player_name = False

	current_game_day = ""
	current_game_details = None

	def handle_starttag(self,tag,attrs):
		if tag == "div" and not self.in_schedule and len(attrs) > 0:
			if attrs[0][0] == "id" and attrs[0][1] == "schedule-page":
				self.in_schedule = True	

		elif self.in_schedule and tag == "button" and self.week == "" and len(attrs) > 1:
			if attrs[0][0] == "class" and attrs[0][1] == "button-filter med dropdown-toggle":
				self.grab_week = True

		elif self.in_schedule and self.grab_games == False and tag == "div" and len(attrs) == 1:
			if attrs[0][0] == "id" and attrs[0][1] == "sched-container":
				self.grab_games = True

		elif self.grab_games and tag == "h2" and len(attrs) > 0:
			if attrs[0][0] == "class" and attrs[0][1] == "table-caption":
				self.grab_game_day = True

		elif self.grab_games and tag == "tr" and len(attrs) > 1 and not self.in_game:
			if attrs[0][0] == "class" and (attrs[0][1] == "even" or attrs[0][1] == "odd"):
				self.reset_flags()

		elif self.in_game and tag == "td" and len(attrs) > 0:
			if attrs[0][0] == "class" and attrs[0][1] == "live":
				self.current_game_details["time"] = "LIVE"

			elif attrs[0][0] == "class":
				if attrs[0][1] == "" and self.grab_away_team == False:
					self.grab_home_team = False
					self.grab_away_team = True

				if attrs[0][1] == "home" and self.grab_home_team == False:
					self.grab_home_team = True
					self.grab_away_team = False

				if attrs[0][1] == "network":
					self.grab_network = True

			elif attrs[0][0] == "data-behavior" and attrs[0][1] == "date_time":
				game_time = datetime.strptime(attrs[1][1].replace("Z",""),"%Y-%m-%dT%H:%M") - timedelta(hours=5)
				self.current_game_details["time"] = game_time.strftime("%I:%M %p EST")

		elif tag == "a" and len(attrs) > 1:
			if self.grab_network and attrs[0][0] == "name" and attrs[1][0] == "href":
				if "schedule" in attrs[0][1] and "espn" in attrs[1][1]:
					self.grab_network = False
					self.current_game_details["broadcast"] = "ESPN"

			elif not self.grab_network and "score" in attrs[0][1] and "game" in attrs[1][1]:
				self.grab_score = True

			elif not self.grab_network and "player" in attrs[0][1] and "player" in attrs[1][1]:
				if "player-details" not in self.current_game_details:
					self.current_game_details["player-details"] = []
				self.grab_player = True
				self.grab_player_name = True

		elif self.in_game and tag == "img" and len(attrs) > 1:
			if attrs[0][0] == "src" and attrs[1][0] == "class" and attrs[1][1] == "schedule-team-logo":
				if self.grab_away_team:
					self.current_game_details["away-image"] = attrs[0][1]

				if self.grab_home_team:
					self.current_game_details["home-image"] = attrs[0][1]

		elif self.in_game and tag == "abbr" and (self.grab_away_team or self.grab_home_team) and not self.grab_abbr:
			self.grab_abbr = True

	def handle_data(self,data):
		if self.grab_week and ("Week" in data or "Bowl" in data or "Wild" in data or "Divisional" in data or "Conference" in data):
			self.grab_week = False
			self.week = data

		elif self.grab_game_day:
			self.grab_game_day = False
			self.current_game_day = data

			if self.current_game_day not in self.games:
				self.games[self.current_game_day] = []

			if self.current_game_day not in self.game_day_order:
				self.game_day_order.append(self.current_game_day)

		elif self.grab_abbr:
			self.grab_abbr = False

			if self.grab_away_team:
				self.current_game_details["away-abbr"] = data

			if self.grab_home_team:
				self.current_game_details["home-abbr"] = data

		elif self.grab_network:
			self.grab_network = False
			self.current_game_details["broadcast"] = data

		elif self.grab_score:
			self.grab_score = False
			self.current_game_details["score"] = data

		elif self.grab_player:
			if self.grab_player_name:
				self.grab_player_name = False
				self.current_game_details["player-details"].append(data)

			else:
				self.current_game_details["player-details"][len(self.current_game_details["player-details"])-1] += data

	def handle_endtag(self,tag):
		if tag == "tr" and self.in_game:
			if "broadcast" in self.current_game_details or "score" in self.current_game_details:
				self.games[self.current_game_day].append(self.current_game_details)
			self.in_game = False

		elif tag == "td" and self.grab_player:
			self.grab_player = False

	def reset_flags(self):
		self.grab_away_team = False
		self.grab_home_team = False
		self.grab_abbr = False
		self.grab_network = False
		self.grab_score = False
		self.grab_player = False
		self.in_game = True
		self.current_game_details = {}

class NFLParser(HTMLParser):

	game_details = None
	games = []

	in_day = False
	grab_day = False
	current_game_day = ""

	in_schedule = False
	in_time = False
	in_time_suff = False
	grabbed_suff = 0

	week = ""
	in_week = False
	in_week_selected = False

	def handle_starttag(self,tag,attrs):
		if tag == "div":
			div_class = attrs[0]
			if "class" == div_class[0] and "schedules-list-hd pre" in div_class[1]:
				self.in_schedule = True
				self.game_details = {}

			elif "class" == div_class[0] and "schedules-list-content pre" in div_class[1]:
				self.in_schedule = False

				self.game_details["home"] = attrs[3][1]
				self.game_details["away"] = attrs[2][1]

				if self.game_details not in self.games and self.current_game_day != "":
					self.games.append(self.game_details)

				self.game_details = None

		if tag == "span" and len(attrs) == 2 and self.in_schedule:
			span_class = attrs[0]
			if "class" == span_class[0] and "nflicon" in span_class[1]:
				self.game_details["broadcast"] = attrs[1][1]

		if tag == "span" and len(attrs) == 1 and self.in_schedule:
			span_class = attrs[0]
			if "class" == span_class[0]:
				if "time" == span_class[1]:
					self.in_time = True
				elif "suff" == span_class[1] and not self.in_time_suff:
					self.in_time = False
					self.in_time_suff = True
				elif self.in_time_suff:
					self.game_details["time"] += " "
					self.game_details["time"] += span_class[1].upper()
					self.grabbed_suff += 1
					if (self.grabbed_suff == 2):
						self.in_time_suff = False
						self.grabbed_suff = 0

		if tag == "li" and len(attrs) == 1:
			li_class = attrs[0]
			if li_class[0] == "class" and li_class[1] == "schedules-list-date":
				self.in_day = True
		if tag == "span" and self.in_day and len(attrs) == 0:
			self.grab_day = True


		if tag == "a" and self.in_week:
			self.in_week_selected = True

	def handle_endtag(self,tag):
		if self.in_time:
			self.in_time = False

	def handle_data(self,data):
		if self.grab_day and self.in_day:
			self.grab_day = False
			self.in_day = False
			self.current_game_day = data.split(",")[0]

		if self.in_time:
			self.game_details["time"] = self.current_game_day+", "+data
		elif self.in_week and self.in_week_selected:
			self.week = data
			self.in_week = False
			self.in_week_selected = False

