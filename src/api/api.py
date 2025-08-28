from fastapi import APIRouter

from src.model.train import train
from src.model.evaluate import evaluate
from src.model.inference import infer


router = APIRouter()


@router.post("/train")
async def api_train():
    print("Calling TRAIN endpoint.")
    score = train()
    return {"Status": "Success", "Score": score}


@router.post("/inference")
async def api_inference():
    print("Calling INFERENCE endpoint.")
    pred = infer()
    return {"Status": "Success", "Prediction": pred}


@router.post("/evaluate")
async def api_evaluate():
    print("Calling EVALUATE endpoint.")
    score = evaluate()
    return {"Status": "Success", "Score": score}