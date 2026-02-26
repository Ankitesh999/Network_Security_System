import sys, os, certifi
from dotenv import load_dotenv
import pymongo

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

ca = certifi.where()
load_dotenv()

mongodb_uri = os.getenv("MONGO_DB_URI")

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd


client = pymongo.MongoClient(mongodb_uri, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
@app.get("/")
async def index():    
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        raise custom_exception(str(e), sys)
    
@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("./final_model/preprocessor.pkl")
        model = load_object("./final_model/model.pkl")

        prediction = NetworkModel(preprocessor, model)
        print(df.iloc[0])

        y_pred = prediction.predict(df)
        print(y_pred)

        df['prediction'] = y_pred
        print(df["prediction"])

        df.to_csv("./prediction_output/prediction.csv")

        table_html = df.to_html(classes="table table-striped")

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        raise custom_exception(str(e), sys)


if __name__ == "__main__" :
    app_run(app, host="0.0.0.0", port=8000)
