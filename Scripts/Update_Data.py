
import re
import numpy as np
import math

from Types.Match import build_match
from Types.Team import build_team
from Types.Ranking import Rank, Rankings

import TBA
import DB_Access as db
from Process_Data import build_score_matrix, solve_matrix, get_labeled_metrics, get_prob
from datetime import datetime, timedelta



def get_as_date(date)   :
    return datetime.strptime(date, '%Y-%m-%d')


def update_events(force_update = False):
    today = datetime.now()
    raw_events, is_updated = TBA.get('/events/2022')
    event_list = []
    for event in raw_events:
        try:
            start = get_as_date(event['start_date']) - timedelta(days = 1)
            end = get_as_date(event['end_date']) + timedelta(days = 1)
            #if event['event_code'] == 'code':
            #if today >= start:
            if today >= start and today <= end or force_update: # code event['event_code'] == 'week0': #
                event_list.append(event['key'])
                db.update_one('events', event)

        except Exception as e:
            message = f"Error in Query_TBA.py. Unable to Query {event['event_code']}"
            db.log_msg(message)

    return event_list

            
    
def update_matches(event_code, force_update = False):
    matches, is_updated = TBA.get('/event/'+event_code+'/matches')
    max_match_num = 0
    match_num_regex = re.compile("m[0-9]+")
    db_matches = []
    for match in matches:
        db_match = build_match(match)
        span = match_num_regex.search(match["key"]).span()
        match_num = float(match["key"][span[0]+1:span[1]])
        if match_num > max_match_num:
            max_match_num = match_num
        if db_match is not None:
            as_dict = db_match.dict() # Force the pydantic type for type checking
            db.update_one('matches', as_dict)
            db_matches.append(as_dict)
    return db_matches


def update_teams(event_code, force_update = False):
    teams, is_updated = TBA.get("/event/"+event_code+"/teams")
    db_teams = []
    for team in teams:
        team_lookup = db.find_one('teams', team["key"][3:])
        if force_update or team_lookup is None or team_lookup['opr'] == 0:
            db_team = build_team(team) # Force the pydantic type for type checking
            if db_team is not None:
                as_dict = db_team.dict()
                db.update_one('teams', as_dict)
                db_teams.append(as_dict)
        else:
            db_teams.append(team_lookup)
    db_teams = sorted(db_teams, key=lambda k: float(k['key']))

    event = db.find_one('events',event_code)
    event['teams'] = teams
    db.update_one('events', event)

    return db_teams


def update_calculations(event_code, matches, teams, opr_coeffecients, force_update = False, ):
    rankings, is_updated = TBA.get("/event/"+event_code+"/rankings")
    team_list = [float(team['key']) for team in teams]
    team_array, score_array = build_score_matrix(event_code, team_list, matches)
    labeled_metrics = get_labeled_metrics(team_list, matches)
    event_started = True
    if np.count_nonzero(score_array)==0:
        event_started = False
    #    db.log_msg(f"Data Array is Empty for {event_code}. Exiting")
    #    return
    
    #team_powers = IRLS(score_array, team_array,1)
    team_powers = solve_matrix(team_array,score_array)
    
    estimator_scores = team_array @ team_powers
    estimator_error = np.square(score_array - estimator_scores) # Compute Squared Errors
    team_variances = solve_matrix(team_array, estimator_error) # Compute Each Teams contribution to squared error
    
    # Fill in Missing Data as best as possible
    skip_update = set()
    for team in zip(teams, team_powers, labeled_metrics):
        #print(team)
        # No Data for this team at this event yet
        if np.count_nonzero(team[2]) == 0 and np.count_nonzero(team[1]) == 0:
            
            #Check if they have played a previous event
            previous_event_entry = db.find_one('teams', team[0]['key'])
            if previous_event_entry is not None and previous_event_entry['opr'] is not None:
                print('Loading from Previous Event', team[0]['key'])
                team[1][1] = previous_event_entry['auto_pr'] / 4.0
                team[1][3] = previous_event_entry['cargo_pr'] / 2.0
                team[2][0] = previous_event_entry['climb_pr']
                team[2][1] = previous_event_entry['taxi_pr']
                skip_update.add(team[0]['key'])
            else:
                print('Loading from Archive', team[0]['key'])
                archive_entry = db.find_one('Archive', team[0]['key'], database = 'pf-database')
                if archive_entry is not None and archive_entry['opr'] is not None:
                    normalized_opr = (clean_num(archive_entry['opr']) * 0.75)
                    normalized_stats = map_opr(normalized_opr, opr_coeffecients)
                    team[2][0] = normalized_stats[3] # Taxi
                    team[1][1] = normalized_stats[2] / 4.0 # Auto
                    team[1][3] = normalized_stats[1] / 2.0 # Cargo                    
                    team[2][1] = normalized_stats[0] # Climb
    
                

    team_powers[np.isnan(team_powers)] = 0
    team_powers = np.around(team_powers,decimals = 2)

    team_variances[np.isnan(team_variances)] = 0

    index = 0


    opr_matrix = team_powers[:,0] * 2 + team_powers[:,1] * 4 + team_powers[:,2] + team_powers[:,3] * 2 + labeled_metrics[:,0] + labeled_metrics[:,1]
    
    if opr_matrix.shape[0] == 0:
        return

    max_opr = np.max(opr_matrix)
    for team in teams:
        opr = opr_matrix[index]
        pr = 100 * (opr/max_opr)

        try:
            
            team['power'] = pr
            team['opr'] = opr
            team['opr_var'] = 0
            team['auto_pr'] = team_powers[index,0] * 2 + team_powers[index,1] * 4 + labeled_metrics[index,1]
            team['auto_pr_var'] = 0
            team['taxi_pr'] = labeled_metrics[index,1]
            team['taxi_pr_var'] = labeled_metrics[index,3]
            team['cargo_pr'] = team_powers[index,2] + team_powers[index,3] * 2
            team['cargo_pr_var'] = 0
            team['cargo_count_pr'] =team_powers[index,0] + team_powers[index,1] + team_powers[index,2] + team_powers[index,3]
            team['cargo_count_pr_var'] = 0
            team['climb_pr'] = labeled_metrics[index,0]
            team['climb_pr_var'] = labeled_metrics[index,2]
            team['fouls'] = team_powers[index,4]
            index +=1
            
            if team['key'] not in skip_update:
                print('Updating Team', team['key'])
                db.update_one('teams', team)
            
        except Exception as e:
            db.log_msg("Issue Updating Team Power Rankings"+ str(team)+ str(e))
        
    
    # Update Rankings Table
    try:
        table = []
        teams = np.array(team_list)
        if rankings is not None:
            for ranking in rankings["rankings"]:
                team = float((ranking["team_key"])[3:])
                index = np.searchsorted(teams, team)
                opr = opr_matrix[index]
                
                pr = 100 * (opr/max_opr)
                rank = float(ranking["rank"])
                row = {
                    "team": team,
                    "rank": rank,
                    "opr": opr,
                    "auto":team_powers[index,0] * 2 + team_powers[index,1] * 4 + labeled_metrics[index,1],
                    "climb":labeled_metrics[index,0],
                    "cargo": team_powers[index,2] + team_powers[index,3] * 2,
                    "cargo_count":team_powers[index,0] + team_powers[index,1] + team_powers[index,2] + team_powers[index,3],
                    "fouls":team_powers[index,4],
                    "power":pr}
                table.append(Rank(**row))
        else:
            for team in teams:
                index = np.searchsorted(teams, team)
                opr = opr_matrix[index]
                
                pr = 100 * (opr/max_opr)
                row = {
                    "team": team,
                    "rank": 0,
                    "opr": opr,
                    "auto":team_powers[index,0] * 2 + team_powers[index,1] * 4 + labeled_metrics[index,1],
                    "climb":labeled_metrics[index,0],
                    "cargo": team_powers[index,2] + team_powers[index,3] * 2,
                    "cargo_count":team_powers[index,0] + team_powers[index,1] + team_powers[index,2] + team_powers[index,3],
                    "fouls":team_powers[index,4],
                    "power":pr
                }
                table.append(Rank(**row))
        rankings = Rankings(**{'key': event_code, 'rankings':table})
        db.update_one('rankings', rankings.dict())                          
            
    except Exception as e:
        db.log_msg("Issue Updating Event Update Time", event_code, str(e))
        raise

def clean_num(num):
    if num is None:
        return 0
    else:
        return float(num)



def update_match_predictions(event, matches, teams):
    for match in matches:
        if match['results'] == 'Predicted':

            predicted_blue_cells = 0
            predicted_red_cells = 0
            
            predicted_blue_endgame = 0
            predicted_red_endgame = 0

            blue_variance = 0
            red_variance = 0
            
            match["blue_extra_rp"] = 0
            match["red_extra_rp"] = 0

            blue_climb_variance = 0
            red_climb_variance = 0

            for i in range(0,3):
                try:
                    blue_team = db.find_one('teams', match['blue'+str(i)])
                    red_team = db.find_one('teams', match['red'+str(i)])

                    match["blue_score"] += clean_num(blue_team["opr"])
                    match["blue_auto_score"] += clean_num(blue_team["auto_pr"])
                    match["blue_endgame_score"] += clean_num(blue_team["climb_pr"])
                    match["blue_teleop_score"] += clean_num(blue_team["cargo_pr"])

                    blue_variance += clean_num(blue_team['auto_pr_var']) + clean_num(blue_team["cargo_pr_var"]) +  clean_num(blue_team['climb_pr_var'])


                    match["red_score"] += clean_num(red_team["opr"])
                    match["red_auto_score"] += clean_num(red_team["auto_pr"])
                    match["red_endgame_score"] += clean_num(red_team["climb_pr"])
                    match["red_teleop_score"] += clean_num(red_team["cargo_pr"])

                    red_variance += clean_num(red_team['auto_pr_var']) + clean_num(red_team["cargo_pr_var"]) +  clean_num(red_team['climb_pr_var'])


                    predicted_blue_cells += clean_num(blue_team["cargo_count_pr"])
                    predicted_blue_endgame += clean_num(blue_team["climb_pr"])
                    blue_climb_variance += clean_num(blue_team["climb_pr_var"])

                    predicted_red_cells += clean_num(red_team["cargo_count_pr"])
                    predicted_red_endgame += clean_num(red_team["climb_pr"])
                    red_climb_variance += clean_num(red_team["climb_pr_var"])

                except Exception as e:
                    print('Unable to Update Event Predictions')
                    db.log_msg("Issue Updating Event Match Predictions", event +  str(e))
                    

            if predicted_blue_endgame >= 16:
                match["blue_hanger_rp"] = 1
                match["blue_rp"] +=1

            if predicted_blue_cells >= 20:
                match["blue_cargo_rp"] = 1
                match["blue_rp"] +=1


            if predicted_red_endgame >= 16:
                match["red_hanger_rp"] = 1
                match["red_rp"] +=1
                
            if predicted_red_cells >= 20:
                match["red_cargo_rp"] = 1
                match["red_rp"] +=1

            match["predicted_blue_score"] = clean_num(match["blue_score"])
            match["predicted_red_score"] = clean_num(match["red_score"])

            win_margin = match["blue_score"] - match["red_score"]
            win_variance = blue_variance + red_variance

            if win_variance >0:
                #win_prob = 0.5 * math.erfc(-win_margin/math.sqrt(2*win_variance))
                win_prob = get_prob(win_margin, win_variance)
            else:
                win_prob = 0.99999

            if match["blue_score"] > match["red_score"]:
                match["blue_rp"] +=2
                match["win_prob"] = win_prob
            elif match["red_score"] > match["blue_score"]:
                match["red_rp"] +=2
                match["win_prob"] = 1 - win_prob
            else:
                match["blue_rp"] +=1
                match["red_rp"] +=1
                match["win_prob"] = 0

            db.update_one('matches', match)

def update_rank_predictions(matches, teams):
    rps = {}
    if len(matches) !=0:
        for match in matches:
            if match['results'] == 'Actual':
                for i in range(0,3):
                    blue_team = match['blue'+str(i)]
                    if blue_team in rps:
                        rps[blue_team] += 0
                    else:
                        rps[blue_team] = 0

            else:
                pass
    else:
        pass

def update_opr_distribution_mapping():
    data = db.find('teams',{})
    if data is not None:
        teams = list(data)
        use_teams = []


        for team in teams:
            if team['opr_var'] is not None:
                use_teams.append(team)

        opr = np.zeros([len(use_teams),1])
        metrics = np.zeros([len(use_teams),4])

        for i, team in enumerate(use_teams):
            
            opr[i] = team['opr']
            metrics[i][0] = team['taxi_pr']
            metrics[i][1] = team['auto_pr']
            metrics[i][2] = team['cargo_pr']
            metrics[i][3] = team['climb_pr']
            #print(team, metrics[i])
        

        #print(metrics)
        coeffecients = np.linalg.pinv(opr) @ metrics
        return coeffecients[0]

def map_opr(opr, coeffecients):
    scores = opr * coeffecients
    if scores[0] > 2:
        scores[2] += scores[0] - 2
        scores[0] = 2
    if scores[3] > 15:
        scores[2] += scores[3] - 15
        scores[3] = 15
      
    return scores
        



def update_data():
    if(TBA.check_connection()):
        force_update = False
        events = update_events(force_update = force_update)
        opr_coeffecients = update_opr_distribution_mapping()

        for event in events:
            matches = update_matches(event, force_update= force_update)
            teams = update_teams(event, force_update = force_update)
            update_calculations(event, matches, teams, opr_coeffecients, force_update = force_update)
            update_match_predictions(event, matches, teams)
            #update_rank_predictions(matches, teams)
        #    print(matches)

if __name__ == '__main__':
    update_data()
    #print(db.find_one('Archive', '1410', database = 'pf-database'))
        
