import numpy as np
from scipy.optimize import nnls
import math

def get_prob(mean, variance):
    return 0.5 * math.erfc(-mean/math.sqrt(2*variance))

# A is the condition Matrix
# y is the output matrix
# p is the order norm to solve with
def IRLS(y, A, p):
    x = np.random.rand(A.shape[1],y.shape[1])
    last_error = float("inf")
    
    iterations = 0
    while iterations < 10:
        e = y - np.matmul(A,  x)
        e_len = e.shape[0]
        w = np.power(e,(p-2)/2)
        W = np.matmul(w,np.linalg.pinv(np.array([sum(w)])))
        W = np.diag(W[:,0])
        
        x_new = np.matmul(np.matmul(np.matmul(np.linalg.pinv(np.matmul(np.matmul(A.T,W),A)),A.T),W),y)
        error = np.linalg.norm(y - np.matmul(A,x_new),p)
        if error < last_error:
            x = x_new
            last_error = error
        else:
            break
        iterations +=1
    return x

def calc_schedule_strengths(event_key, match_data, teams, team_powers, num_matches):
    schedules = np.zeros(len(teams),1)
    teams = np.array(teams)
    for i in range(0, num_matches):
        key_str = event_key+"_qm" + str(i+1)
        match = match_data.get_item(Key={'key': key_str})
        match = match["Item"]
        
        b0 = np.searchsorted(teams, float(match["blue"+str(0)]))
        b1 = np.searchsorted(teams, float(match["blue"+str(1)]))
        b2 = np.searchsorted(teams, float(match["blue"+str(2)]))
        
        r0 = np.searchsorted(teams, float(match["red"+str(0)]))
        r1 = np.searchsorted(teams, float(match["red"+str(1)]))
        r2 = np.searchsorted(teams, float(match["red"+str(2)]))
        
def safe_div(a, b):
    if b != 0:
        return a/b
    else:
        return 0
    
    
def build_score_matrix(event_key, teams, matches):
    num_teams = len(teams)
    metrics = ["auto_cargo_lower","auto_cargo_upper","teleop_cargo_lower","teleop_cargo_upper","fouls"]
    num_matches = len(matches)
    teams = np.array(teams)
    team_array = np.zeros([num_matches*2,num_teams])
    score_array = np.zeros([num_matches*2,len(metrics)])

    i = 0
    for match in matches:
        if match["results"] == "Actual":
            metric_count = 0
            for metric in metrics:
                score_array[i][metric_count] = match["blue_" + metric]
                score_array[num_matches + i][metric_count] = match["red_" + metric]
                metric_count +=1
            
            for j in range(0,3):
                blue_index = np.searchsorted(teams, float(match["blue"+str(j)]))
                red_index = np.searchsorted(teams, float(match["red"+str(j)]))
                team_array[i][blue_index] = 1
                team_array[num_matches+i][red_index] = 1
                
            i+=1

    return team_array, score_array
    
def get_labeled_metrics(teams, matches):
    #Endgame Columns: None, Mid, Traversal, Low, High
    #Taxi Columns: Yes, No
    #Endgame array columns: Expected Taxi Points,Expected Climb Points, Taxi Variance, Climb Variance
    
    team_results = {}


    for match in matches:
        if match["results"] == "Actual":
            for j in range(0,3):
                blue_team = match["blue"+str(j)]
                red_team = match["red"+str(j)]

                if blue_team not in team_results:
                    team_results[blue_team] = {'climbs':[], 'taxis':[]}
                if red_team not in team_results:
                    team_results[red_team] = {'climbs':[], 'taxis':[]}

                if match["blue_endgame_robot"+str(j+1)] == "None":
                    team_results[blue_team]['climbs'].append(0)
                elif match["blue_endgame_robot"+str(j+1)] == "Low":
                    team_results[blue_team]['climbs'].append(4)
                elif match["blue_endgame_robot"+str(j+1)] == "Mid":
                    team_results[blue_team]['climbs'].append(6)
                elif match["blue_endgame_robot"+str(j+1)] == "High":
                    team_results[blue_team]['climbs'].append(10)
                elif match["blue_endgame_robot"+str(j+1)] == "Traversal":
                    team_results[blue_team]['climbs'].append(15)
                else:
                    team_results[blue_team]['climbs'].append(0)

                if match["blue_taxi_robot"+str(j+1)] == "No":
                    team_results[blue_team]['taxis'].append(0)
                elif match["blue_taxi_robot"+str(j+1)] == "Yes":
                    team_results[blue_team]['taxis'].append(2)


                if match["red_endgame_robot"+str(j+1)] == "None":
                    team_results[red_team]['climbs'].append(0)
                elif match["red_endgame_robot"+str(j+1)] == "Low":
                    team_results[red_team]['climbs'].append(4)
                elif match["red_endgame_robot"+str(j+1)] == "Mid":
                    team_results[red_team]['climbs'].append(6)
                elif match["red_endgame_robot"+str(j+1)] == "High":
                    team_results[red_team]['climbs'].append(10)
                elif match["red_endgame_robot"+str(j+1)] == "Traversal":
                    team_results[red_team]['climbs'].append(15)
                else:
                    team_results[red_team]['climbs'].append(0)

                if match["red_taxi_robot"+str(j+1)] == "No":
                    team_results[red_team]['taxis'].append(0)
                elif match["red_taxi_robot"+str(j+1)] == "Yes":
                    team_results[red_team]['taxis'].append(2)


    metrics_array = np.zeros([len(teams),4])
    for team in team_results.keys():
        metrics = team_results[team]     
        index = np.searchsorted(teams, team)

        climbs = np.array(metrics['climbs'])
        taxis = np.array(metrics['taxis'])
        metrics_array[index][0] = np.average(climbs)
        metrics_array[index][1] = np.average(taxis)
        metrics_array[index][2] = np.var(climbs)
        metrics_array[index][3] = np.var(taxis)
    return metrics_array

def solve_matrix(matrix, solution):
    num_teams = matrix.shape[1]
    num_equations = matrix.shape[0]
    
    if num_equations > num_teams:
        X = np.zeros([matrix.shape[1],solution.shape[1]])
        for i in range(0,solution.shape[1]):
            X[:,i] = nnls(matrix,solution[:,i])[0]
        return X
    else:
        return np.linalg.lstsq(matrix,solution,rcond=None)[0]
        pass
