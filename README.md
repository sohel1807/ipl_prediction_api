# IPL Win Predictor API

This API predicts the winning probabilities of an IPL match based on the current game situation.

## Endpoint

**URL:** `https://sohel1807--predict.modal.run`
**Method:** `POST`
**Content-Type:** `application/json`

## Request

### Sample Input

```json
{
    "batting_team": "Chennai Super Kings",
    "bowling_team": "Royal Challengers Bangalore",
    "city": "Bengaluru",
    "total_runs": 120,
    "current_score": 110,
    "wickets": 5,
    "overs_completed": 12.0
}
