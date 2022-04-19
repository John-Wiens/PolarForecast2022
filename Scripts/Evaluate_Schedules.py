import numpy as np
import pickle
import random

def save_temp(data, name):
    with open(name, 'wb') as f:
        pickle.dump(data, f)

def load_temp(name):
    with open(name, 'rb') as f:
        return pickle.load(f)



matches = load_temp( 'matches.pickle')
teams = load_temp( 'teams.pickle')
event = load_temp( 'event.pickle')


def get_random_team(team_list, exclude_teams = []):
    index = int(random.random() * len(team_list))
    team = team_list[index]
    while team in exclude_teams:
        index = int(random.random() * len(team_list))
        team = team_list[index]

    return team

def get_random_alliances(team_list):
    blue1 = get_random_team(team_list)
    blue2 = get_random_team(team_list, exclude_teams=[blue1])
    blue3 = get_random_team(team_list, exclude_teams=[blue1, blue2])
    red1 = get_random_team(team_list, exclude_teams=[blue1, blue2, blue3])
    red2 = get_random_team(team_list, exclude_teams=[blue1, blue2, blue3, red1])
    red3 = get_random_team(team_list, exclude_teams=[blue1, blue2, blue3, red1, red2])
    return [blue1, blue2, blue3], [red1, red2, red3]

def get_alliance_metrics(alliance, teams):
    score = 0
    climb = 0
    cargo = 0
    for team in alliance:
        score += teams[team]['opr']
        climb += teams[team]['climb_pr']
        cargo += teams[team]['cargo_pr']

    return score, climb, cargo
    
def simulate_event(teams, team_list, num_matches):
    rps = {}
    for j in range(0, num_matches):
        blue_alliance, red_alliance = get_random_alliances(team_list)
        
        blue_score, blue_climb, blue_cargo = get_alliance_metrics(blue_alliance, teams)
        red_score, red_climb, red_cargo = get_alliance_metrics(red_alliance, teams)

        blue_rp = 0
        red_rp = 0


        if blue_climb >= 16:
            blue_rp +=1
        if blue_cargo >= 20:
            blue_rp +=1

        if red_climb >= 16:
            red_rp +=1
        if red_cargo >= 20:
            red_rp +=1
        
        if blue_score > red_score:
            blue_rp += 2
        elif red_score > blue_score:
            red_rp +=2
        else:
            blue_rp +=1
            red_rp +=1
        
        for team in blue_alliance:
            if team in rps:
                rps[team] += blue_rp
            else:
                rps[team] = blue_rp

        for team in red_alliance:
            if team in rps:
                rps[team] += red_rp
            else:
                rps[team] = red_rp
    return rps


def evaluate_schedules(event, matches, teams):
    team_rps = {}
    team_list = []
    team_dict = {}
    for team in teams:
        if team['key'] not in team_rps:
            team_list.append(int(team['key']))
            team_rps[int(team['key'])] = {'RP': 0, 'Simulated': []}
            team_dict[int(team['key'])] = team

    teams = team_dict
    qual_matches = 0
    for match in matches:
        if match['comp_level'] == 'qm':
            qual_matches +=1
            for i in range(0,3):
                team_rps[match['blue{}'.format(i)]]['RP'] += match['blue_rp']
                team_rps[match['red{}'.format(i)]]['RP'] += match['red_rp']
            
    
    for i in range(0,10000):
        rps = simulate_event(teams,team_list, qual_matches)
        for team in rps.keys():
            team_rps[team]['Simulated'].append(rps[team])

    
    for team in team_rps.keys():
        results = np.array(team_rps[team]['Simulated'])
        predicted = team_rps[team]['RP']
        average = np.average(results)
        high = np.max(results)
        low = np.min(results)
        strength = predicted - average

        team_rps[team]['average'] = average
        team_rps[team]['high'] = high
        team_rps[team]['low'] = low
        team_rps[team]['strength'] = strength
        print("Team: {}, Predicted RP: {}, Average Schedule RP: {}, Schedule Strength: {}".format(team, predicted, average, strength ))

    new_rankings = dict(sorted(team_rps.items(), key=lambda item: item[1]['average'], reverse = True))

    for i, rank in enumerate(new_rankings.keys()):
        team = rank
        predicted = new_rankings[rank]['RP']
        average = new_rankings[rank]['average']
        strength = new_rankings[rank]['strength']
        print("Rank: {:4}, Team: {:4}, Predicted RP: {:4}, Average Schedule RP: {:4.4}, Schedule Strength: {:4.4}".format(i+1, team, predicted, average, strength ))

    new_rankings = dict(sorted(team_rps.items(), key=lambda item: item[1]['strength'], reverse = True))

    for i, rank in enumerate(new_rankings.keys()):
        team = rank
        predicted = new_rankings[rank]['RP']
        average = new_rankings[rank]['average']
        strength = new_rankings[rank]['strength']
        print("Rank: {:4}, Team: {:4}, Predicted RP: {:4}, Average Schedule RP: {:4.4}, Schedule Strength: {:4.4}".format(i+1, team, predicted, average, strength ))

           

    
if __name__ == '__main__':
    evaluate_schedules(event, matches, teams)
