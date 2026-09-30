"""KBC hackathon proof of concept: predict a customer's situation from app behaviour."""

import json
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, StringConstraints

# The model always looks at the most recent N actions (sliding window).
WINDOW_SIZE = 5


# --- Vocabulary: add new actions or outcomes here -----------------------------

class Action(str, Enum):
    APP_OPENED = "APP_OPENED"
    APP_CLOSED = "APP_CLOSED"
    APP_REFRESHED = "APP_REFRESHED"


class Prediction(str, Enum):
    USER_NEUTRAL = "USER_NEUTRAL"
    USER_STRESSED = "USER_STRESSED"


# --- Demo data: in production this comes from KBC's existing app logs ---------

USERS: dict[str, list[Action]] = {
    "aaa-aaa-aaa-aaa": [Action.APP_OPENED, Action.APP_REFRESHED, Action.APP_OPENED, Action.APP_CLOSED],
    "bbb-bbb-bbb-bbb": [Action.APP_OPENED, Action.APP_CLOSED, Action.APP_OPENED, Action.APP_CLOSED, Action.APP_OPENED],
    "ccc-ccc-ccc-ccc": [Action.APP_OPENED, Action.APP_REFRESHED, Action.APP_REFRESHED, Action.APP_REFRESHED, Action.APP_REFRESHED],
}


# --- The "AI model" ------------------------------------------------------------

class Predictor(ABC):
    """Any model (rules today, machine learning tomorrow) must implement this."""

    @abstractmethod
    def predict(self, actions: list[Action]) -> tuple[Prediction, str]:
        """Return the prediction and a short human-readable reason."""


class RuleBasedPredictor(Predictor):
    """Simple rule: frequent refreshing means the customer may need help."""

    REFRESH_THRESHOLD = 3

    def predict(self, actions: list[Action]) -> tuple[Prediction, str]:
        if not actions:
            return Prediction.USER_NEUTRAL, "Geen recente acties gevonden."

        refreshes = actions.count(Action.APP_REFRESHED)
        reason = f"{refreshes} keer refresh in de laatste {len(actions)} acties."

        if refreshes >= self.REFRESH_THRESHOLD:
            return Prediction.USER_STRESSED, reason
        return Prediction.USER_NEUTRAL, reason


# Swap this line for an ML model later; the API stays exactly the same.
predictor: Predictor = RuleBasedPredictor()


# --- API ---------------------------------------------------------------------

app = FastAPI(title="KBC Behaviour Analysis")


class AnalysisRequest(BaseModel):
    user_uuid: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class AnalysisResponse(BaseModel):
    user_uuid: str
    analysed_actions: list[Action]
    prediction: Prediction
    reason: str


def error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(RequestValidationError)
async def invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
    return error(400, "INVALID_REQUEST", 'Body must be JSON like {"user_uuid": "aaa-aaa-aaa-aaa"}.')


@app.post("/api/v1/behaviour-analysis", response_model=AnalysisResponse)
def behaviour_analysis(body: AnalysisRequest):
    if body.user_uuid not in USERS:
        return error(404, "USER_NOT_FOUND", f"No user found with uuid '{body.user_uuid}'.")

    recent_actions = USERS[body.user_uuid][-WINDOW_SIZE:]
    prediction, reason = predictor.predict(recent_actions)

    return AnalysisResponse(
        user_uuid=body.user_uuid,
        analysed_actions=recent_actions,
        prediction=prediction,
        reason=reason,
    )


# --- Demo frontend (a web page, not an API endpoint) ---------------------------

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def frontend() -> str:
    # The page gets the demo users' action history injected, so the data lives in one place.
    html = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
    # Escape "<" so the data can never close the <script> tag it is injected into.
    return html.replace("__USERS__", json.dumps(USERS).replace("<", "\\u003c"))
