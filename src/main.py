from fastapi import FastAPI

from src.model.train import train


app = FastAPI()


@app.post("/train")
async def api_train():
    print("Calling TRAIN endpoint.")
    score = train()
    return {"Status": "Success", "Score": score}


@app.get("/inference")
async def api_inference():
    print("Calling INFERENCE endpoint.")


@app.get("/evaluate")
async def api_evaluate():
    print("Calling EVALUATE endpoint.")
