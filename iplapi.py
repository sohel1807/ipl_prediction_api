# Fast api server for ipl win prediction
from fastapi import FastAPI
import pandas as pd
import pickle
from pydantic import BaseModel


pipe = pickle.load(open("pipe.pkl", "rb"))


app = FastAPI()

class PredictInput(BaseModel):
    batting_team: str
    bowling_team: str
    city: str
    total_runs: int
    current_score: int
    wickets: int
    overs_completed: float

@app.get("/")
def simple():
    return {"hello every one"}

@app.post("/predict")
def predict(data: PredictInput):
    
    runs_left = data.total_runs - data.current_score
    balls_left = 120 - (data.overs_completed * 6)
    wickets_left = 10 - data.wickets
    crr = data.current_score / (data.overs_completed + 1)
    rrr = (runs_left * 6) / balls_left

    final_data = pd.DataFrame({
        "BattingTeam": [data.batting_team],
        "BowlingTeam": [data.bowling_team],
        "City": [data.city],
        "runs_left": [runs_left],
        "total_run_y": [data.total_runs],
        "balls_left": [balls_left],
        "wickets_left": [wickets_left],
        "CRR": [crr],
        "RRR": [rrr]
    })

    result = pipe.predict_proba(final_data)

    if data.current_score >= data.total_runs:
        batting_team_prob = 100.0
        bowling_team_prob = 0.0
    elif wickets_left == 0:
        batting_team_prob = 0.0
        bowling_team_prob = 100.0
    else:
        batting_team_prob = round(result[0][1] * 100, 2)
        bowling_team_prob = round(result[0][0] * 100, 2)

    return {
        data.batting_team: batting_team_prob,
        data.bowling_team : bowling_team_prob
    }