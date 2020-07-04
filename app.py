import logging

import uvicorn
#from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
#from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from rest_api.config import DB_HOST, DB_USER, DB_PW, DB_PORT, ES_CONN_SCHEME, APM_SERVER, APM_SERVICE_NAME
from rest_api.controller.errors.http_error import http_error_handler
from rest_api.controller.router import router as api_router

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)
logging.getLogger("qa-app").setLevel(logging.WARNING)

'''elasticsearch_client = Elasticsearch(
    hosts=[{"host": DB_HOST, "port": DB_PORT}], http_auth=(DB_USER, DB_PW), scheme=ES_CONN_SCHEME, ca_certs=False, verify_certs=False
)'''


def get_application() -> FastAPI:
    application = FastAPI(title="Haystack-API", debug=True, version="0.1")

    application.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )

    if APM_SERVER:
        apm_config = {"SERVICE_NAME": APM_SERVICE_NAME, "SERVER_URL": APM_SERVER, "CAPTURE_BODY": "all"}
        elasticapm = make_apm_client(apm_config)
        application.add_middleware(ElasticAPM, client=elasticapm)

    application.add_exception_handler(HTTPException, http_error_handler)

    application.include_router(api_router)

    return application


app = get_application()

logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")
logger.info(
    """
Or just try it out directly: curl --request POST --url 'http://127.0.0.1:8000/models/1/doc-qa' --data '{"questions": ["What is the capital of Germany?"]}'
"""
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
