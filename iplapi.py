from modal import Stub, build, enter, method, web_endpoint, Image, Mount
from typing import Dict
import pandas as pd
import pickle

image = Image.debian_slim().pip_install(
    "scikit-learn",
    "pandas"
)

stub = Stub(name="ipl_prediction", image=image)

@stub.function(mounts=[Mount.from_local_file("pipe.pkl", remote_path='/root/pipe.pkl')])
@web_endpoint(label="predict", method="POST")
def predict_percentage(Info: Dict):
    with open('/root/pipe.pkl', 'rb') as f:
        data = pickle.load(f)
        
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

    result = data.predict_proba(final_data)

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
