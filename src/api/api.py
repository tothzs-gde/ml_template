import traceback
from fastapi import APIRouter
from fastapi import HTTPException

from src.api.api_models import InferenceRequest
from src.model.datadrift import check_drift
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
    logger.info("Calling TRAIN endpoint.")
    try:
        run_name, new_model_name, new_model_version = train(
            model_name=model_name,
            model_version=model_version,
        )
        return {
            "run_name": run_name,
            "registered_model_name": new_model_name,
            "registered_model_version": new_model_version,
            "status": "success",
        }
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="Training failed due to an internal error.",
        )


@router.post("/inference")
async def api_inference(
    request: InferenceRequest,
    model_name: str = settings.mlflow_registered_model_name,
    model_version: str = "latest",
):
    logger.info("Calling INFERENCE endpoint.")
    try:
        predictions = infer(
            X_data = request.data,
            model_name=model_name,
            model_version=model_version,
        )
        return {"status": "success", "prediction": predictions}
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="Inference failed due to an internal error.",
        )


@router.post("/evaluate")
async def api_evaluate(
    model_name: str = settings.mlflow_registered_model_name,
    model_version: str = "latest",
):
    logger.info("Calling EVALUATE endpoint.")
    try:
        score = evaluate(
            model_name=model_name,
            model_version=model_version,
        )
        return {"status": "success", "model_performance": score}
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="Evaluation failed due to an internal error.",
        )


@router.get("/health")
def health_check():
    logger.info("Calling HEALTH endpoint.")
    return {"status": "ok"}


@router.post("/drift")
async def api_evaluate():
    logger.info("Calling DRIFT endpoint.")
    try:
        drift_results = check_drift()

        for key in drift_results:
            drift_results[key]["drifted"] = str(drift_results[key]["drifted"])

        return {"status": "success", "drift_results": drift_results}
    except Exception as e:
        logger.error(e.with_traceback(e.__traceback__))
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="Drift detection failed due to an internal error.",
        )