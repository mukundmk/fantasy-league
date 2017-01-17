import os
import json

from app import app
from flask import render_template
from collections import defaultdict
from xlrd import open_workbook


@app.route('/')
def index():
    with open(app.config['JSON_FILE']) as f:
        data = json.load(f)

    if data['version'] == -1:
        if os.path.isfile(app.config['FIXTURES_FILE']):
            with open(app.config['FIXTURES_FILE']) as f:
                for l in f:
                    line = [x.strip() for x in l.strip().split(',')]

                    if len(line) == 3:
                        week, team1, team2 = line
                        if int(week) <= app.config['WEEKS']:
                            if week not in data['fixtures']:
                                data['fixtures'][week] = list()

                            data['fixtures'][week].append(
                                {'team1': team1, 'team2': team2, 'score_team1': '', 'score_team2': '', 'winner': 'NA'})

                            if team1 not in data['teams']:
                                data['scoreboard'].append(
                                    {'team': team1, 'wins': 0, 'losses': 0, 'draws': 0, 'points': 0})
                                data['teams'].append(team1)

                            if team2 not in data['teams']:
                                data['scoreboard'].append(
                                    {'team': team2, 'wins': 0, 'losses': 0, 'draws': 0, 'points': 0})
                                data['teams'].append(team2)

                    else:
                        week, team1, team2, team3 = line
                        if int(week) <= app.config['WEEKS']:
                            if week not in data['fixtures']:
                                data['fixtures'][week] = list()

                            data['fixtures'][week].append(
                                {'team1': team1, 'team2': team2, 'team3': team3, 'score_team1': '', 'score_team2': '',
                                 'score_team3': '', 'winner': 'NA'})

                            if team1 not in data['teams']:
                                data['scoreboard'].append(
                                    {'team': team1, 'wins': 0, 'losses': 0, 'draws': 0, 'points': 0})
                                data['teams'].append(team1)

                            if team2 not in data['teams']:
                                data['scoreboard'].append(
                                    {'team': team2, 'wins': 0, 'losses': 0, 'draws': 0, 'points': 0})
                                data['teams'].append(team2)

                            if team3 not in data['teams']:
                                data['scoreboard'].append(
                                    {'team': team3, 'wins': 0, 'losses': 0, 'draws': 0, 'points': 0})
                                data['teams'].append(team3)

            data['version'] += 1

            with open(app.config['JSON_FILE'], 'w') as f:
                json.dump(data, f)

    if data['version'] < app.config['WEEKS']:
        while os.path.isfile(app.config['WEEKLY_FILES'][data['version']]):
            sheet = open_workbook(app.config['WEEKLY_FILES'][data['version']]).sheets()[0]
            d = defaultdict(int)
            for row in range(1, sheet.nrows):
                d[sheet.cell(row, 0).value.strip()] += int(sheet.cell(row, 2).value) + int(sheet.cell(row, 3).value) + \
                                                       int(5 * sheet.cell(row, 4).value) + \
                                                       int(17 * sheet.cell(row, 5).value) + \
                                                       int(5 * sheet.cell(row, 6).value)

            for fixture in data['fixtures'][str(data['version'] + 1)]:
                score1 = d[fixture['team1']]
                score2 = d[fixture['team2']]
                score3 = d[fixture['team3']] if 'team3' in fixture else -1

                fixture['score_team1'] = score1
                fixture['score_team2'] = score2
                if score3 > -1:
                    fixture['score_team3'] = score3

                if score1 > score2 and score1 > score3:
                    fixture['winner'] = fixture['team1']
                    for row in data['scoreboard']:
                        if row['team'] == fixture['team1']:
                            row['wins'] += 1
                            row['points'] += 3

                        if row['team'] == fixture['team2']:
                            row['losses'] += 1

                        if score3 > -1 and row['team'] == fixture['team3']:
                            row['losses'] += 1

                elif score2 > score1 and score2 > score3:
                    fixture['winner'] = fixture['team2']
                    for row in data['scoreboard']:
                        if row['team'] == fixture['team1']:
                            row['losses'] += 1

                        if row['team'] == fixture['team2']:
                            row['wins'] += 1
                            row['points'] += 3

                        if score3 > -1 and row['team'] == fixture['team3']:
                            row['losses'] += 1

                elif score3 > score1 and score3 > score2:
                    fixture['winner'] = fixture['team3']
                    for row in data['scoreboard']:
                        if row['team'] == fixture['team1']:
                            row['losses'] += 1

                        if row['team'] == fixture['team2']:
                            row['losses'] += 1

                        if row['team'] == fixture['team3']:
                            row['wins'] += 1
                            row['points'] += 3

                else:
                    fixture['winner'] = 'Draw'

                    if score1 == score2 == score3:
                        for row in data['scoreboard']:
                            if row['team'] == fixture['team1']:
                                row['draws'] += 1
                                row['points'] += 1

                            if row['team'] == fixture['team2']:
                                row['draws'] += 1
                                row['points'] += 1

                            if row['team'] == fixture['team3']:
                                row['draws'] += 1
                                row['points'] += 1

                    if score1 == score2:
                        for row in data['scoreboard']:
                            if row['team'] == fixture['team1']:
                                row['draws'] += 1
                                row['points'] += 1

                            if row['team'] == fixture['team2']:
                                row['draws'] += 1
                                row['points'] += 1

                            if score3 > -1 and row['team'] == fixture['team3']:
                                row['losses'] += 1

                    if score1 == score3:
                        for row in data['scoreboard']:
                            if row['team'] == fixture['team1']:
                                row['draws'] += 1
                                row['points'] += 1

                            if row['team'] == fixture['team2']:
                                row['losses'] += 1

                            if row['team'] == fixture['team3']:
                                row['draws'] += 1
                                row['points'] += 1

                    if score2 == score3:
                        for row in data['scoreboard']:
                            if row['team'] == fixture['team1']:
                                row['losses'] += 1

                            if row['team'] == fixture['team2']:
                                row['draws'] += 1
                                row['points'] += 1

                            if row['team'] == fixture['team3']:
                                row['draws'] += 1
                                row['points'] += 1

            data['version'] += 1
            data['scoreboard'].sort(key=lambda x: x['points'], reverse=True)

            with open(app.config['JSON_FILE'], 'w') as f:
                json.dump(data, f)

            if data['version'] >= app.config['WEEKS']:
                break

    if data['version'] == app.config['WEEKS']:
        data['playoffs'][0]['team1'] = data['scoreboard'][2]['team']
        data['playoffs'][1]['team1'] = data['scoreboard'][3]['team']
        data['playoffs'][1]['team2'] = data['scoreboard'][4]['team']
        data['playoffs'][2]['team1'] = data['scoreboard'][0]['team']
        data['playoffs'][3]['team1'] = data['scoreboard'][1]['team']

        data['version'] += 1

        with open(app.config['JSON_FILE'], 'w') as f:
            json.dump(data, f)

    if data['version'] == app.config['WEEKS'] + 1:
        if os.path.isfile(app.config['PLAYOFFS_FILE']):
            sheet = open_workbook(app.config['PLAYOFFS_FILE']).sheets()[0]
            d = defaultdict(int)
            for row in range(1, sheet.nrows):
                d[sheet.cell(row, 0).value.strip()] += int(sheet.cell(row, 2).value) + int(sheet.cell(row, 3).value) + \
                                                       int(5 * sheet.cell(row, 4).value) + \
                                                       int(17 * sheet.cell(row, 5).value) + \
                                                       int(5 * sheet.cell(row, 6).value)

            data['playoffs'][0]['score_team1'] = d[data['playoffs'][0]['team1']]
            data['playoffs'][0]['score_team2'] = d[data['playoffs'][0]['team2']]
            data['playoffs'][1]['score_team1'] = d[data['playoffs'][1]['team1']]
            data['playoffs'][1]['score_team2'] = d[data['playoffs'][1]['team2']]

            if data['playoffs'][0]['score_team1'] > data['playoffs'][0]['score_team2']:
                data['playoffs'][0]['winner'] = data['playoffs'][0]['team1']
                data['playoffs'][2]['team2'] = data['playoffs'][0]['team1']

            else:
                data['playoffs'][0]['winner'] = data['playoffs'][0]['team2']
                data['playoffs'][2]['team2'] = data['playoffs'][0]['team2']

            if data['playoffs'][1]['score_team1'] > data['playoffs'][1]['score_team2']:
                data['playoffs'][1]['winner'] = data['playoffs'][1]['team1']
                data['playoffs'][3]['team2'] = data['playoffs'][1]['team1']

            else:
                data['playoffs'][1]['winner'] = data['playoffs'][1]['team2']
                data['playoffs'][3]['team2'] = data['playoffs'][1]['team2']

            data['version'] += 1

            with open(app.config['JSON_FILE'], 'w') as f:
                json.dump(data, f)

    if data['version'] == app.config['WEEKS'] + 2:
        if os.path.isfile(app.config['PLAYOFFS2_FILE']):
            sheet = open_workbook(app.config['PLAYOFFS2_FILE']).sheets()[0]
            d = defaultdict(int)
            for row in range(1, sheet.nrows):
                d[sheet.cell(row, 0).value.strip()] += int(sheet.cell(row, 2).value) + int(sheet.cell(row, 3).value) + \
                                                       int(5 * sheet.cell(row, 4).value) + \
                                                       int(17 * sheet.cell(row, 5).value) + \
                                                       int(5 * sheet.cell(row, 6).value)

            data['playoffs'][2]['score_team1'] = d[data['playoffs'][2]['team1']]
            data['playoffs'][2]['score_team2'] = d[data['playoffs'][2]['team2']]
            data['playoffs'][3]['score_team1'] = d[data['playoffs'][3]['team1']]
            data['playoffs'][3]['score_team2'] = d[data['playoffs'][3]['team2']]

            if data['playoffs'][2]['score_team1'] > data['playoffs'][2]['score_team2']:
                data['playoffs'][2]['winner'] = data['playoffs'][2]['team1']
                data['playoffs'][4]['team1'] = data['playoffs'][2]['team1']

            else:
                data['playoffs'][2]['winner'] = data['playoffs'][2]['team2']
                data['playoffs'][4]['team1'] = data['playoffs'][2]['team2']

            if data['playoffs'][3]['score_team1'] > data['playoffs'][3]['score_team2']:
                data['playoffs'][3]['winner'] = data['playoffs'][3]['team1']
                data['playoffs'][4]['team2'] = data['playoffs'][3]['team1']

            else:
                data['playoffs'][3]['winner'] = data['playoffs'][3]['team2']
                data['playoffs'][4]['team2'] = data['playoffs'][3]['team2']

            data['version'] += 1

            with open(app.config['JSON_FILE'], 'w') as f:
                json.dump(data, f)

    if data['version'] == app.config['WEEKS'] + 3:
        if os.path.isfile(app.config['FINALS_FILE']):
            sheet = open_workbook(app.config['FINALS_FILE']).sheets()[0]
            d = defaultdict(int)
            for row in range(1, sheet.nrows):
                d[sheet.cell(row, 0).value.strip()] += int(sheet.cell(row, 2).value) + int(sheet.cell(row, 3).value) + \
                                                       int(5 * sheet.cell(row, 4).value) + \
                                                       int(17 * sheet.cell(row, 5).value) + \
                                                       int(5 * sheet.cell(row, 6).value)

            data['playoffs'][4]['score_team1'] = d[data['playoffs'][4]['team1']]
            data['playoffs'][4]['score_team2'] = d[data['playoffs'][4]['team2']]

            if data['playoffs'][4]['score_team1'] > data['playoffs'][4]['score_team2']:
                data['playoffs'][4]['winner'] = data['playoffs'][4]['team1']

            else:
                data['playoffs'][4]['winner'] = data['playoffs'][4]['team2']

            data['version'] += 1

            with open(app.config['JSON_FILE'], 'w') as f:
                json.dump(data, f)

    win_sp = 'color:white;background:#38003c;border:1px solid #38003c;'
    win_fc = 'border:1px solid #38003c;'
    return render_template('index.html', data=data, win_sp=win_sp, win_fc=win_fc, weeks=app.config['WEEKS'])
