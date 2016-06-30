import praw
import re
import csv
from collections import defaultdict, Counter, OrderedDict

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

r = praw.Reddit(user_agent='theMusicOfReddit')

listOfComments = []
allComments = []
justSubreddits = []

# Number of tracks you wish to fetch from each subreddit
nTracks = 50

totalSubmissiosn = 0


# Splits on '-' for posts following "artist - song" schema
# Parses and cleans data (removing useless posts)

def getComments(subreddit, amount):
    print("Grabbing " + subreddit)
    submissions = r.get_subreddit(subreddit).get_top_from_all(limit=amount)
    for submission in submissions:
        submission.replace_more_comments(limit=2, threshold=0)
        comments = praw.helpers.flatten_tree(submission.comments)
        for comment in comments:
            if not hasattr(comment, 'author'):
                continue
            if str(comment.author) == 'None':
                continue
            allComments.append([str(comment.author), subreddit, str(comment.score)])

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
    getComments(sub, nTracks)

# Restructures listOfTracks in to a dictionary, d
d = defaultdict(set)
for a,b, c  in allComments:
    d[a].add(b)

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

currentStart = 0
for i in subredditList:
    currentStart += 1
    for j in subredditList:
        if i == j or subredditList.index(j) < currentStart:
            continue
        checkOccurances(d, i, j)

# Outputs data to CSV in Gephi readable format
#print("Writing to CSV...")
with open('mydata.csv', 'w', newline='') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    for row in data:
        thedatawriter.writerow(row)

with open('allcomments.csv', 'w', newline='') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    for row in allComments:
        thedatawriter.writerow(row)

print("CSV output done!")