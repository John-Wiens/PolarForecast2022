

import DB_Access as db
import glob
import json

for f in glob.glob('./historical_data/*.json'):
    print(f)
    with open(f, 'r') as datafile:
        for line in datafile.readlines():
            print(line)
            json_data = json.loads(line)
            
            break

'''
def update_teams(event_code, force_update = False):
    teams, is_updated = TBA.get("/event/"+event_code+"/teams")
    db_teams = []
    for team in teams:
        db_team = build_team(team) # Force the pydantic type for type checking
        if db_team is not None:
            as_dict = db_team.dict()
            db.update_one('teams', as_dict)
            db_teams.append(as_dict)

    db_teams = sorted(db_teams, key=lambda k: float(k['key']))

    event = db.find_one('events',event_code)
    event['teams'] = teams
    db.update_one('events', event)

    return db_teams
    '''