from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TraininPipelineConfig
import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TraininPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

        logging.info("Initiate Data ingestion")
    except Exception as e:
        raise NetworkSecurityException(e,sys)