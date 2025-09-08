import traceback
from fastapi import APIRouter

from src.model.train import train
from src.model.evaluate import evaluate
from src.model.inference import infer
from src.utils.logging import logger
from src.utils.settings import settings


router = APIRouter()


@router.post("/train")
async def api_train(
    model_name: str = settings.mlflow_registered_model_name,
    model_version: str = "latest",
):
    print("Calling TRAIN endpoint.")
    try:
        train(
            model_name=model_name,
            model_version=model_version,
        )
        return {"status": "success"}
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        return {"status": "failed"}


@router.post("/inference")
async def api_inference(
    model_name: str = settings.mlflow_registered_model_name,
    model_version: str = "latest",
):
    print("Calling INFERENCE endpoint.")
    try:
        pred = infer(
            model_name=model_name,
            model_version=model_version,
        )
        return {"status": "success", "prediction": pred}
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        return {"status": "failed"}


@router.post("/evaluate")
async def api_evaluate(
    model_name: str = settings.mlflow_registered_model_name,
    model_version: str = "latest",
):
    print("Calling EVALUATE endpoint.")
    try:
        score = evaluate(
            model_name=model_name,
            model_version=model_version,
        )
        return {"status": "success", "accuracy_score": score}
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        return {"status": "failed"}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/drift")
async def api_evaluate():
    pass