

import TBA
import json
import random




def get_match_team_climb(match, team):
    if team in match['alliances']['blue']['team_keys']:
        color = 'blue'
    else:
        color = 'red'

    index = match['alliances'][color]['team_keys'].index(team)
    if match['score_breakdown'] is not None:
        climb_status = match['score_breakdown'][color]['endgameRobot{}'.format(index +1)]
        return climb_status
    else:
        return 'Empty'

    

def get_climb_abilities():
    climb_ability = {}
    teams, success = TBA.get('/event/2022okok/teams/keys')
    for team in teams:
        events, event_success = TBA.get('/team/{}/events/keys'.format(team))

        climb_ability[team] = {'2020_climbs':0, '2020_attempts':0, '2019_climbs':0, '2019_attempts':0, 'climb_high':0}

        for event in events:
            if event[0:4] == '2020':
                matches, matches_success = TBA.get('/team/{}/event/{}/matches'.format(team, event))
                for match in matches:
                    climb_status = get_match_team_climb(match, team)
                    if climb_status == 'Hang':
                        climb_ability[team]['2020_climbs'] += 1
                        climb_ability[team]['2020_attempts'] += 1
                    
                        
                    if climb_status != 'Empty':
                        climb_ability[team]['2020_attempts'] += 1

                    
                    

            if event[0:4] == '2019':
                matches, matches_success = TBA.get('/team/{}/event/{}/matches'.format(team, event))
                for match in matches:
                    climb_status = get_match_team_climb(match, team)

                    
                    if climb_status == 'HabLevel2':
                        climb_ability[team]['2019_climbs'] += 1
                    elif climb_status == 'HabLevel3':
                        climb_ability[team]['2019_climbs'] += 1
                        climb_ability[team]['climb_high'] += 1

                    if climb_status != 'Empty':
                        climb_ability[team]['2019_attempts'] += 1

    return climb_ability

#abilities = get_climb_abilities()
#with open('climb_abilities.json','w') as f:
#    f.write(json.dumps(abilities))
with open('climb_abilities.json','r') as f:
    climb_abilities = json.loads(f.read())


def get_climb_rewards(climb_abilities):
    climb_rewards = []
    rookies = []
    sum_effectiveness = 0
    sum_teams = 0
    for team in climb_abilities.keys():
        effectiveness = 0
        reward = 0
        if climb_abilities[team]['2020_attempts'] != 0:
            effectiveness = climb_abilities[team]['2020_climbs'] / climb_abilities[team]['2020_attempts']
            sum_effectiveness += effectiveness
            sum_teams +=1
        elif climb_abilities[team]['2019_attempts'] != 0:
            effectiveness = climb_abilities[team]['2019_climbs'] / climb_abilities[team]['2019_attempts']
            sum_effectiveness += effectiveness
            sum_teams +=1
        else:
            rookies.append(team)
            pass
        
        if climb_abilities[team]['2019_attempts'] != 0:
            if climb_abilities[team]['climb_high']/climb_abilities[team]['2019_attempts'] > 0.2:
                reward = 10
            else:
                reward = 6
        else:
            reward = 6
        
        climb_rewards.append({'reward': reward, 'chance':effectiveness, 'team': team})
    for team in rookies:
        climb_rewards.append({'reward': 6, 'chance': sum_effectiveness / sum_teams,'team': team})

        
    return climb_rewards

climb_rewards = get_climb_rewards(climb_abilities)
print(climb_rewards)

def simulate_climbs(trials, success_chance, rewards, climb_rewards):
    success = 0
    for i in range(0,trials):
        robot2 = climb_rewards[int(random.random() * len(climb_rewards))]
        robot3 = climb_rewards[int(random.random() * len(climb_rewards))]

        score = 0
        if success_chance > random.random():
            score += rewards
        if robot2['chance'] > random.random():
            score += robot2['reward']
        if robot3['chance'] > random.random():
            score += robot3['reward']
        
        if score > 16:
            success +=1
    return success / trials


for i in range(0,11):
    print(str(i/10.0),simulate_climbs(100000, i/10.0, 6, climb_rewards),simulate_climbs(100000, i/10.0, 10, climb_rewards))

