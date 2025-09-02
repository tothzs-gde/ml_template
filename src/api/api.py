from fastapi import APIRouter

from src.model.train import train
# from src.model.evaluate import evaluate
# from src.model.inference import infer


router = APIRouter()


@router.post("/train")
async def api_train():
    print("Calling TRAIN endpoint.")
    try:
        train()
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed"}


# @router.post("/inference")
# async def api_inference():
#     print("Calling INFERENCE endpoint.")
#     pred = infer()
#     return {"status": "success", "prediction": pred}


# @router.post("/evaluate")
# async def api_evaluate():
#     print("Calling EVALUATE endpoint.")
#     score = evaluate()
#     return {"status": "success", "score": score}