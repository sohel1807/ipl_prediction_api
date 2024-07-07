from fastapi import FastAPI, Body
from typing import Dict
import pickle
import pandas as pd

app = FastAPI()

with open('pipe.pkl', 'rb') as f:
    model = pickle.load(f)

@app.post("/predict")
def predict_percentage(Info: Dict = Body(...)):
    batting_team = Info["batting_team"]
    bowling_team = Info["bowling_team"]
    city = Info["city"]
    total_runs = Info["total_runs"]
    current_score = Info["current_score"]
    wickets = Info["wickets"]
    overs_completed = Info["overs_completed"]

    runs_left = total_runs - current_score
    balls_left = 120 - (overs_completed * 6)
    wickets_left = 10 - wickets
    crr = current_score / (overs_completed + 1)
    rrr = (runs_left * 6) / balls_left

    final_data = pd.DataFrame({
        "BattingTeam": [batting_team],
        "BowlingTeam": [bowling_team],
        "City": [city],
        "runs_left": [runs_left],
        "total_run_y": [total_runs],
        "balls_left": [balls_left],
        "wickets_left": [wickets_left],
        "CRR": [crr],
        "RRR": [rrr]
    })

    result = model.predict_proba(final_data)

    if current_score >= total_runs:
        batting_team_prob = 100.0
        bowling_team_prob = 0.0
    elif wickets_left == 0:
        batting_team_prob = 0.0
        bowling_team_prob = 100.0
    else:
        batting_team_prob = round(result[0][1] * 100, 2)
        bowling_team_prob = round(result[0][0] * 100, 2)

    return {
        batting_team: batting_team_prob,
        bowling_team: bowling_team_prob
    }