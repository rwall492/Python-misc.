import scrapy
from tutorial.items import GameItem
from tutorial.items import TextItem
from tutorial.items import PlayerItem
import csv

writer = csv.writer(open('output.csv','wb'))

def fill(path, array):
    team = GameItem()
    team['name'] = path.xpath("div[@class='team-capsule']/p/a/text()").extract()
    team['final'] = path.xpath("ul[@class='score']/li[@class='final']/text()").extract()
    array.append(team)

def fill_player(path, array):
    player = PlayerItem()
#    player['opponent'] = path.xpath("li[@class='team-name']/a/text()").extract()
    player['stats1'] = path.xpath("td[@class='textright']/text()").extract()
    player['stats2'] = path.xpath("td[@class='textright bleft']/text()").extract()
    player['opponent'] = path.xpath("td/ul[@class='game-schedule']/li[@class='team-name']/a/text()").extract()
    player['result'] = path.xpath("td/a/text()").extract()
    array.append(player)

def fill_text(array, path1, path2, name):
    text = TextItem()

    text['stuff'] = path1.xpath("text()").extract()
    text['owner'] = path1.xpath("a/text()").extract()
    text['player'] = path1.xpath("b/a/text()").extract()
    text['date'] = path2.xpath("nobr/span[@class='recent-activity-date']/text()").extract()
    array.append(text)

    temp = []    
    for x in array[0]['stuff']:
        if "Trophy" not in x:
            temp.append(x)

    print temp

    with open("%s.txt" % name,"w") as file:
        file.write("Last transaction on: %s.\n\n" % (array[0]['date'][0]))
        
        for x in range(len(array[0]['player'])):
            file.write("%s%s.\n" % (array[0]['player'][x], temp[2*x]))

class League1Spider(scrapy.Spider):
    #scrapy crawl text to execute
    name = "league1"
    allowed_domains = ["espn.go.com/"]
    
    def start_requests(self):
        yield self.make_requests_from_url("http://games.espn.go.com/ffl/leagueoffice?leagueId=224263&seasonId=2015")
    
    def parse(self, response):
        sel = scrapy.Selector(response)
        path1 = sel.xpath("//li[@class='recent-activity-description']")
        path2 = sel.xpath("//li[@class='recent-activity-when']")
        entries = []

        fill_text(entries, path1, path2, "league1")

class League2Spider(scrapy.Spider):
    #scrapy crawl text to execute
    name = "league2"
    allowed_domains = ["espn.go.com/"]
    
    def start_requests(self):
        yield self.make_requests_from_url("http://games.espn.go.com/ffl/leagueoffice?leagueId=479865&seasonId=2015")
    
    def parse(self, response):
        sel = scrapy.Selector(response)
        path1 = sel.xpath("//li[@class='recent-activity-description']")
        path2 = sel.xpath("//li[@class='recent-activity-when']")
        entries = []

        fill_text(entries, path1, path2, "league2")

class League3Spider(scrapy.Spider):
    #scrapy crawl text to execute
    name = "league3"
    allowed_domains = ["espn.go.com/"]
    
    def start_requests(self):
        yield self.make_requests_from_url("http://games.espn.go.com/ffl/leagueoffice?leagueId=557055&seasonId=2015")
    
    def parse(self, response):
        sel = scrapy.Selector(response)
        path1 = sel.xpath("//li[@class='recent-activity-description']")
        path2 = sel.xpath("//li[@class='recent-activity-when']")
        entries = []

        fill_text(entries, path1, path2, "league3")

class League4Spider(scrapy.Spider):
    #scrapy crawl text to execute
    name = "league4"
    allowed_domains = ["espn.go.com/"]
    
    def start_requests(self):
        yield self.make_requests_from_url("http://games.espn.go.com/ffl/leagueoffice?leagueId=786559&seasonId=2015")
    
    def parse(self, response):
        sel = scrapy.Selector(response)
        path1 = sel.xpath("//li[@class='recent-activity-description']")
        path2 = sel.xpath("//li[@class='recent-activity-when']")
        entries = []

        fill_text(entries, path1, path2, "league4")

class PlayerSpider(scrapy.Spider):
    name = "player"
    allowed_domains = ["espn.go.com"]

    def start_requests(self):
        input = csv.reader(open('players.csv'))
        
        for x in input:
            for y in range(0,15):
                years = 2000 + y
                yield self.make_requests_from_url("http://espn.go.com/nfl/player/gamelog/_/id/%s/year/%d/%s" % (x[1],years,x[0]))

    def parse(self, response):
        sel = scrapy.Selector(response)
        path = sel.xpath("//tr[contains(@class,'row team')]")
        items = []

        player_id = 0
        year = 0

        player_id = response.url[43:48]
        year = response.url[54:58]

        fill_player(path,items)

        games = len(items[0]['result'])
        print games, len(items[0]['stats1']), len(items[0]['stats2'])

        for x in range(games):
            writer.writerow([player_id,year,items[0]['opponent'][x], items[0]['result'][x], items[0]['stats1'][10*x + 0], items[0]['stats1'][10*x + 1], items[0]['stats1'][10*x + 2], items[0]['stats1'][10*x + 3], items[0]['stats1'][10*x + 4], items[0]['stats1'][10*x + 5], items[0]['stats1'][10*x + 6], items[0]['stats1'][10*x + 7], items[0]['stats1'][10*x + 8], items[0]['stats1'][10*x + 9], items[0]['stats2'][2*x + 0], items[0]['stats2'][2*x + 1]])

class BasicSpider(scrapy.Spider):
    name = "basic"

    allowed_domains = ["espn.go.com"]

    def start_requests(self):
        for j in range(2006,2015):
            for i in range(1,18):
                yield self.make_requests_from_url("http://espn.go.com/nfl/scoreboard?seasonYear=%d&seasonType=2&weekNumber=%d" % (j, i))

    def parse(self, response):
        sel = scrapy.Selector(response)

        year = response.url[45:49]

        if response.url[-2] == "=":
            week = response.url[-1]
        else:
            week = response.url[-2:]

        visitor = sel.xpath("//div[@class='team visitor']")
        home = sel.xpath("//div[@class='team home']")

        items_v = []
        items_h = []

        fill(visitor,items_v)
        fill(home,items_h)

        n_games = len(home)

        for x in range(n_games):
            writer.writerow([year, week , items_h[0]['name'][x] , items_v[0]['name'][x] , items_h[0]['final'][x] , items_v[0]['final'][x]])

class StatsSpider(scrapy.Spider):
    name = "stats"
#    allowed_domains = ["dmoz.org"]
#    start_urls = ["http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"]

    allowed_domains = ["espn.go.com"]

    def start_requests(self):
        for j in range(2006,2015):
            for i in range(1,18):
                yield self.make_requests_from_url("http://espn.go.com/nfl/scoreboard?seasonYear=%d&seasonType=2&weekNumber=%d" % (j, i))

    def parse(self, response):
        sel = scrapy.Selector(response)

        year = response.url[45:49]

        if response.url[-2] == "=":
            week = response.url[-1]
        else:
            week = response.url[-2:]

        visitor = sel.xpath("//div[@class='team visitor']")
        home = sel.xpath("//div[@class='team home']")

        items_v = []
        items_h = []
        
        fill(visitor,items_v)
        fill(home,items_h)

        n_games = len(home)

        for x in range(n_games):
            writer.writerow([year, week , items_h[0]['name'][x] , items_v[0]['name'][x] , items_h[0]['final'][x] , items_v[0]['final'][x]])

