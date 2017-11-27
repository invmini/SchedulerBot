#!/usr/bin/python

import urllib
import urllib2

from HTMLParser import HTMLParser

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


def obtainHTML(url):
	res = urllib2.urlopen(url)
	return res.read()

def createHTMLElement(element,attrs,content):
	html = "<"
	html += element

	for attr in attrs:
		html += " "
		html += attr[0]
		html += "=\""
		html += attr[1]
		html += "\""

	html += ">"
	html += content
	html += "</"
	html += element
	html += ">"

	return html

def createHTMLScheduleHead():

	schedule_header = createHTMLElement("th",[("align","left")],"Time")
	schedule_header += createHTMLElement("th",[("align","center")],"Game")
	schedule_header += createHTMLElement("th",[("align","center")],"Broadcast")

	schedule_row = createHTMLElement("tr",[],schedule_header);

	return createHTMLElement("thead",[],schedule_row)

def createHTMLGameRow(home,away,broadcast,time):

	game_time = createHTMLElement("th",[("align","left")],time)

	game_home = createHTMLElement("a",[("href","/"+home)],"")
	game_away = createHTMLElement("a",[("href","/"+away)],"")
	game_teams = game_away+" @ "+game_home
	game_details = createHTMLElement("td",[("align","center")],game_teams)

	
	game_broadcaster = createHTMLElement("a",[("href","/"+home)],"")
	game_broadcast = createHTMLElement("td",[("align","center")],game_broadcaster)

	return createHTMLElement("tr",[],game_time+game_details+game_broadcast)

def createHTMLScheduleBody(games):

	games_html = ""

	for game in games:
		games_html += createHTMLGameRow(game["home"],game["away"],game["broadcast"],game["time"])

	return createHTMLElement("tbody",[],games_html)

def createHTMLScheduleTable(games):

	html = createHTMLScheduleHead()
	html += createHTMLScheduleBody(games)

	return createHTMLElement("table",[],html)

def main():
	html = obtainHTML("http://www.nfl.com/schedules")

	parser = NFLParser()
	parser.feed(html)

	print parser.week
	print createHTMLScheduleTable(parser.games)

	exit(0)

if __name__ == "__main__":
	main()
