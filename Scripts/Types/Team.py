
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Team(BaseModel):
    # Required Team Metrics
    key: str
    team_number: int
    name: str
    rookie_year: int

    # Statistical Metrics
    power: Optional[float]

    opr: Optional[float]
    opr_var: Optional[float]

    auto_pr: Optional[float]
    auto_pr_var: Optional[float]

    taxi_pr:Optional[float]
    taxi_pr_var: Optional[float]

    cargo_pr: Optional[float]
    cargo_pr_var: Optional[float]

    cargo_count_pr: Optional[float]
    cargo_count_pr_var: Optional[float]

    climb_pr: Optional[float]
    climb_pr_var: Optional[float]

    

    fouls: Optional[float]



    # Interesting Stats to Display
    city:  Optional[str] = ""
    country:  Optional[str] = ""
    school_name: Optional[str] = ""
    state_prov:  Optional[str] = ""
    website:  Optional[str] = ""

def build_team(team):
    team_num = team["key"][3:]
    team["key"] = team_num
    team["name"] = team["nickname"]




    del team["nickname"]
    del team["gmaps_place_id"]
    del team["gmaps_url"]
    del team["lat"]
    del team["lng"]
    del team["postal_code"]
    del team["location_name"]
    del team["address"]
    del team["motto"]
    return Team(**team)

