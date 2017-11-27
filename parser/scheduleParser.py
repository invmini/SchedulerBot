#!/usr/bin/python

import urllib
import urllib2

from HTMLParser import HTMLParser

class NFLParser(HTMLParser):

	in_schedule = False
	game_details = None
	games = []
	in_time = False
	in_time_suff = False
	grabbed_suff = 0

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

				if self.game_details not in self.games:
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

	def handle_endtag(self,tag):
		if self.in_time:
			self.in_time = False


	def handle_data(self,data):
		if self.in_time:
			self.game_details["time"] = data


def obtainHTML(url):
	res = urllib2.urlopen(url)
	return res.read()

def main():
	html = obtainHTML("http://www.nfl.com/schedules")

	parser = NFLParser()
	parser.feed(html)
	print parser.games

	exit(0)

if __name__ == "__main__":
	main()
