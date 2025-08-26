from fastapi import FastAPI

from src.model.train import train
from src.model.evaluate import evaluate
from src.model.inference import infer


app = FastAPI()


@app.post("/train")
async def api_train():
    print("Calling TRAIN endpoint.")
    score = train()
    return {"Status": "Success", "Score": score}


@app.get("/inference")
async def api_inference():
    print("Calling INFERENCE endpoint.")
    pred = infer()
    return {"Status": "Success", "Prediction": pred}


@app.post("/evaluate")
async def api_evaluate():
    print("Calling EVALUATE endpoint.")
    score = evaluate()
    return {"Status": "Success", "Score": score}
