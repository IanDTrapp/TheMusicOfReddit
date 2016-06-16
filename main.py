import praw
import re
import csv
import networkx as nx
from collections import defaultdict, OrderedDict
import itertools
#import matplotlib.pyplot as plt

G = nx.Graph()

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

r = praw.Reddit(user_agent='theMusicOfReddit')

listOfTracks = []

# Number of tracks you wish to fetch from each subreddit
nTracks = 30000

totalSubmissiosn = 0


# Splits on '-' for posts following "artist - song" schema
# Parses and cleans data (removing useless posts)

def getTracks(subreddit, amount):
    print("Grabbing " + subreddit)
    submissions = r.get_subreddit(subreddit).get_top_from_all(limit=amount)
    print("Parsing...")
    for x in submissions:
        if "-" in x.title:
            title = re.sub('\([^)]*\)', '', x.title)
            title = re.sub('\[.*\]', '', title)
            title = title.lower()
            try:
                title.encode('ascii')
            except UnicodeEncodeError:
                continue
            else:
                track = title.split("-")
                if len(track) <= 1 or len(track) > 2:
                    continue
                if len(track[0]) > 40:
                    continue
                if 1459468800 < x.created < 1459555199:
                    continue
                if 1427846400 < x.created < 1427932799:
                    continue
                if 1364774400 < x.created < 1396396799:
                    continue
                if 1396310400 < x.created < 1364860799:
                    continue
                if 1333238400 < x.created < 1333324799:
                    continue
                if 1301616000 < x.created < 1301702399:
                    continue
                if 1270080000 < x.created < 1270166399:
                    continue
                if 1238544000 < x.created < 1238630399:
                    continue
                if 1207008000 < x.created < 1207094399:
                    continue
                track[0] = track[0].strip()
                track[0] = re.sub('([^\s\w]|_)+', '', track[0])
                track[1] = track[1].strip()
                track[1] = re.sub('([^\s\w]|_)+', '', track[1])

                track.append(subreddit)
                listOfTracks.append(track)

# List of subreddits to fetch from
subredditList = ['metalcore', 'hardcore', 'posthardcore', 'metal', 'deathmetal', 'progmetal',
                 'edm', 'dubstep', 'dnb', 'tropicalhouse', 'electronicmusic',
                 'modernrockmusic', 'postrock', 'punk',
                 'hiphopheads', 'trap', 'popheads',
                 'jazz', 'indieheads', 'country', 'ambientmusic', 'blues', 'classicalmusic', 'indiefolk', 'folk',
                 'electrohouse', 'poppunkers', 'rap', 'reggae', 'indie_rock', 'ska', 'trance', 'alternativerock',
                 'doommetal', 'blackmetal', 'djent', 'powermetal', 'deathcore', 'psybient', 'classical', 'chillstep',
                 'triphop', 'hardstyle', 'electroswing', 'melodichardcore', '90shiphop', 'techno', 'swinghouse',
                 'chillmusic', 'psychedelicrock', 'progrockmusic', 'classicrock', 'seashanties', 'postmetal', 'sludge',
                 'stonermetal', 'funk']



subredditList.sort()

for sub in subredditList:
    getTracks(sub, nTracks)

print("Sorting...")
listOfTracks.sort()

# Restructures listOfTracks in to a dictionary, d
d = defaultdict(set)
for a,b, c in listOfTracks:
    d[a].add(c)

# Checks occurances of each subreddit combination in the dictionaries
def checkOccurances(d, genreA, genreB):
    count = 0
    for d in d.items():
        if genreA in (sorted(d[1])) and genreB in (sorted(d[1])):
            count += 1
    if count>0:
        tempRow = []
        print(genreA + " + " + genreB + ": " + str(count))
        # Appends data in a Gephi readable format
        tempRow.append(genreA)
        tempRow.append(genreB)
        tempRow.append('Undirected')
        tempRow.append(str(count))
        data.append(tempRow)

data = []

# Adds titles for Gephi
data.append(['source', 'target', 'type', 'weight'])

# Loops through every combination of subreddits and doesn't permit commutativity
# For example - pop + metal = metal + pop, reduces search time
currentStart = 0
for i in subredditList:
    currentStart += 1
    for j in subredditList:
        if i == j or subredditList.index(j) < currentStart:
            continue
        checkOccurances(d, i, j)

# Outputs data to CSV in Gephi readable format
print("Writing to CSV...")
with open('mydata.csv', 'w', newline='') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    for row in data:
        thedatawriter.writerow(row)

print("CSV output done!")
