#!/usr/bin/python
import sys, argparse
import urllib2
from scheduleFormatter import ScheduleFormatter
from scheduleParser import ESPNParser

nfl_url = "http://www.espn.com/nfl/schedule"
nba_url = "http://www.espn.com/nba/schedule"
ncaaf_url = "http://www.espn.com/college-football/schedule"

nfl_header = "NFL Schedule"
nba_header = "NBA Schedule"
ncaaf_header = "NCAA Football Schedule"

def obtainHTML(url):
	res = urllib2.urlopen(url)
	return res.read()

def main():

	args = argparse.ArgumentParser()
	args.add_argument('--nfl',action='store_true',dest='nfl',help="Create table from ESPN's NFL schedule")
	args.add_argument('--nba',action='store_true',dest='nba',help="Create table from ESPN's NBA schedule")
	args.add_argument('--ncaaf',action='store_true',dest='ncaaf',help="Create table from ESPN's NCAA football schedule")
	args.add_argument('--scores',action='store_true',dest='score',help="Include finished games in table")
	args.add_argument('--schedule',action='store_true',dest='schedule',help="Include future games in table")
	args.add_argument('--date',dest='date',help="Date of schedule to parse, NBA: yearmonthday eg. --nba --date 20171108, NFL: week, eg. --nfl --date 7")

	option = args.parse_args()

	schedule_url = nfl_url
	league_header = ""

	if option.nfl:
		league_header = nfl_header
		schedule_url = nfl_url

	elif option.nba:
		league_header = nba_header
		schedule_url = nba_url

	elif option.ncaaf:
		league_header = ncaaf_header
		schedule_url = ncaaf_url

	else:
		league_header = nfl_header

	if option.date is not None:
		if option.nfl or option.ncaaf:
			schedule_url += "/_/week/" + option.date
		elif option.nba:
			schedule_url += "/_/date/" + option.date

	html = obtainHTML(schedule_url)

	parser = ESPNParser()
	parser.feed(html)

	schedule_results = []
	
	if option.score:
		schedule_results.append(("score","\n\n**Game Results**"))
	if option.schedule:
		schedule_results.append(("time","\n\n**Upcoming Game Schedule**"))

	formatter = ScheduleFormatter()

	print formatter.createRedditScheduleTable(parser,league_header,schedule_results)

	exit(0)

if __name__ == "__main__":
	main()
