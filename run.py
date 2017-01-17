import sys
import json
from app import app

if len(sys.argv) > 1:
    if sys.argv[1] == 'clean':
        data = dict()
        data['version'] = -1
        data['fixtures'] = dict()
        data['teams'] = list()
        data['scoreboard'] = list()
        data['playoffs'] = list()
        data['playoffs'].append({'team1': 'TBD', 'team2': 'TBD', 'score_team1': '', 'score_team2': '', 'winner': ''})
        data['playoffs'].append({'team1': 'TBD', 'team2': 'TBD', 'score_team1': '', 'score_team2': '', 'winner': ''})
        data['playoffs'].append({'team1': 'TBD', 'team2': 'TBD', 'score_team1': '', 'score_team2': '', 'winner': ''})
        data['playoffs'].append({'team1': 'TBD', 'team2': 'TBD', 'score_team1': '', 'score_team2': '', 'winner': ''})
        data['playoffs'].append({'team1': 'TBD', 'team2': 'TBD', 'score_team1': '', 'score_team2': '', 'winner': ''})

        with open(app.config['JSON_FILE'], 'w') as f:
            json.dump(data, f)

    elif sys.argv[1] == 'lucky':
        with open(app.config['JSON_FILE']) as f:
            data = json.load(f)

        data['playoffs'][0]['team2'] = sys.argv[2]

        with open(app.config['JSON_FILE'], 'w') as f:
            json.dump(data, f)

else:
    app.run()
