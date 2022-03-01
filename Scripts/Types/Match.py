from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Match(BaseModel):

    key: str
    update_time: float = datetime.utcnow().timestamp()
    results: str

    comp_level: str
    event_key: str
    match_number: int
    set_number: Optional[int] = 0
    time: Optional[int] = 0
    blue0: int = 0
    red0: int = 0
    blue1: int = 0
    red1: int = 0
    blue2: int = 0
    red2: int = 0

    blue_score: float = 0
    blue_auto_score: float = 0 
    blue_teleop_score: float = 0
    blue_endgame_score: float  = 0
    blue_taxi_robot1: str = ""
    blue_taxi_robot2: str = ""
    blue_taxi_robot3: str = ""
    blue_auto_cargo_lower: float = 0
    blue_auto_cargo_upper: float = 0
    blue_teleop_cargo_lower: float = 0
    blue_teleop_cargo_upper: float = 0
    blue_endgame_robot1: str = ""
    blue_endgame_robot2: str = ""
    blue_endgame_robot3: str = ""
    blue_fouls: float = 0
    blue_rp: float = 0
    blue_cargo_rp: float = 0
    blue_hanger_rp: float = 0

    red_score: float = 0
    red_auto_score: float = 0 
    red_teleop_score: float = 0
    red_endgame_score: float  = 0
    red_taxi_robot1: str = ""
    red_taxi_robot2: str = ""
    red_taxi_robot3: str = ""
    red_auto_cargo_lower: float = 0
    red_auto_cargo_upper: float = 0
    red_teleop_cargo_lower: float = 0
    red_teleop_cargo_upper: float = 0
    red_endgame_robot1: str = ""
    red_endgame_robot2: str = ""
    red_endgame_robot3: str = ""
    red_fouls: float = 0
    red_rp: float = 0
    red_cargo_rp: float = 0
    red_hanger_rp: float = 0



def build_match(match):
    for i in range(0,3):
        match["blue" + str(i)] = match["alliances"]["blue"]["team_keys"][i][3:]
        match["red" + str(i)] = match["alliances"]["red"]["team_keys"][i][3:]
        
    if match["score_breakdown"] != "null" and match["score_breakdown"] is not None:
        # Blue Aggregate Scores  
        match["blue_score"] = match["score_breakdown"]["blue"]["totalPoints"]
        match["blue_auto_score"] = match["score_breakdown"]["blue"]["autoPoints"]
        match["blue_teleop_score"] = match["score_breakdown"]["blue"]["teleopPoints"]
        match["blue_endgame_score"] = match["score_breakdown"]["blue"]["endgamePoints"]

        # Blue Auto Behavior
        match["blue_taxi_robot1"] = match["score_breakdown"]["blue"]["taxiRobot1"]
        match["blue_taxi_robot2"] = match["score_breakdown"]["blue"]["taxiRobot2"]
        match["blue_taxi_robot3"] = match["score_breakdown"]["blue"]["taxiRobot3"]
        
        match["blue_auto_cargo_lower"] = \
            match["score_breakdown"]["blue"]["autoCargoLowerBlue"] + \
            match["score_breakdown"]["blue"]["autoCargoLowerRed"] + \
            match["score_breakdown"]["blue"]["autoCargoLowerFar"] + \
            match["score_breakdown"]["blue"]["autoCargoLowerNear"]

        match["blue_auto_cargo_upper"] = \
            match["score_breakdown"]["blue"]["autoCargoUpperBlue"] + \
            match["score_breakdown"]["blue"]["autoCargoUpperRed"] + \
            match["score_breakdown"]["blue"]["autoCargoUpperFar"] + \
            match["score_breakdown"]["blue"]["autoCargoUpperNear"]

        
        # Blue Teleop Behavior
        match["blue_teleop_cargo_lower"] = \
            match["score_breakdown"]["blue"]["autoCargoLowerBlue"] + \
            match["score_breakdown"]["blue"]["autoCargoLowerRed"] + \
            match["score_breakdown"]["blue"]["autoCargoLowerFar"] + \
            match["score_breakdown"]["blue"]["autoCargoLowerNear"]

        match["blue_teleop_cargo_upper"] = \
            match["score_breakdown"]["blue"]["teleopCargoUpperBlue"] + \
            match["score_breakdown"]["blue"]["teleopCargoUpperRed"] + \
            match["score_breakdown"]["blue"]["teleopCargoUpperFar"] + \
            match["score_breakdown"]["blue"]["teleopCargoUpperNear"]
        
        match["blue_fouls"] = match["score_breakdown"]["blue"]["foulPoints"]

        # Blue Endgame Behavior
        match["blue_endgame_robot1"] = match["score_breakdown"]["blue"]["endgameRobot1"]
        match["blue_endgame_robot2"] = match["score_breakdown"]["blue"]["endgameRobot2"]
        match["blue_endgame_robot3"] = match["score_breakdown"]["blue"]["endgameRobot3"]

        match["blue_cargo_rp"] = float(match["score_breakdown"]["blue"]["cargoBonusRankingPoint"])
        match["blue_hanger_rp"] = float(match["score_breakdown"]["blue"]["hangarBonusRankingPoint"])
        match["blue_rp"] = match["score_breakdown"]["blue"]["rp"]


        # Red Aggregate Scores  
        match["red_score"] = match["score_breakdown"]["red"]["totalPoints"]
        match["red_auto_score"] = match["score_breakdown"]["red"]["autoPoints"]
        match["red_teleop_score"] = match["score_breakdown"]["red"]["teleopPoints"]
        match["red_endgame_score"] = match["score_breakdown"]["red"]["endgamePoints"]

        # Red Auto Behavior
        match["red_taxi_robot1"] = match["score_breakdown"]["red"]["taxiRobot1"]
        match["red_taxi_robot2"] = match["score_breakdown"]["red"]["taxiRobot2"]
        match["red_taxi_robot3"] = match["score_breakdown"]["red"]["taxiRobot3"]
        
        match["red_auto_cargo_lower"] = \
            match["score_breakdown"]["red"]["autoCargoLowerBlue"] + \
            match["score_breakdown"]["red"]["autoCargoLowerRed"] + \
            match["score_breakdown"]["red"]["autoCargoLowerFar"] + \
            match["score_breakdown"]["red"]["autoCargoLowerNear"]

        match["red_auto_cargo_upper"] = \
            match["score_breakdown"]["red"]["autoCargoUpperBlue"] + \
            match["score_breakdown"]["red"]["autoCargoUpperRed"] + \
            match["score_breakdown"]["red"]["autoCargoUpperFar"] + \
            match["score_breakdown"]["red"]["autoCargoUpperNear"]

        
        # Red Teleop Behavior
        match["red_teleop_cargo_lower"] = \
            match["score_breakdown"]["red"]["autoCargoLowerBlue"] + \
            match["score_breakdown"]["red"]["autoCargoLowerRed"] + \
            match["score_breakdown"]["red"]["autoCargoLowerFar"] + \
            match["score_breakdown"]["red"]["autoCargoLowerNear"]

        match["red_teleop_cargo_upper"] = \
            match["score_breakdown"]["red"]["teleopCargoUpperBlue"] + \
            match["score_breakdown"]["red"]["teleopCargoUpperRed"] + \
            match["score_breakdown"]["red"]["teleopCargoUpperFar"] + \
            match["score_breakdown"]["red"]["teleopCargoUpperNear"]
        
        match["red_fouls"] = match["score_breakdown"]["red"]["foulPoints"]

        # Red Endgame Behavior
        match["red_endgame_robot1"] = match["score_breakdown"]["red"]["endgameRobot1"]
        match["red_endgame_robot2"] = match["score_breakdown"]["red"]["endgameRobot2"]
        match["red_endgame_robot3"] = match["score_breakdown"]["red"]["endgameRobot3"]

        match["red_cargo_rp"] = float(match["score_breakdown"]["red"]["cargoBonusRankingPoint"])
        match["red_hanger_rp"] = float(match["score_breakdown"]["red"]["hangarBonusRankingPoint"])
        match["red_rp"] = match["score_breakdown"]["red"]["rp"]



    
        
        match["results"] = "Actual"

    else:
        match["results"] = "Predicted"
        
    del match["alliances"]
    del match["videos"]
    del match["score_breakdown"]
    del match["winning_alliance"]

    db_match = Match(**match)
    return db_match



        