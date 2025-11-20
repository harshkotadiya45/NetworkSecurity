from networksecurity.entity.artifcat_entity import DataIngestionArtifcat, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidationArtifact:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifcat, 
                 Data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.Data_validation_config = Data_validation_config
            self._schema_config_ = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)  
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config_)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe of columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else :
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1, d2)
                if threshold < is_sample_dist.pvalue:
                    is_found = False
                else :
                    is_found = True
                    status = False

                report.update({column : {
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.Data_validation_config.drift_report_file_path

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_data_validation(self) -> DataIngestionArtifcat:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Read Data from train and test
            train_dataframe = DataValidationArtifact.read_data(train_file_path)
            test_dataframe = DataValidationArtifact.read_data(test_file_path)

            #validate number of colummns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"train dataframe does not contain all columns. \n"

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"test dataframe does not contain all columns. \n"

            if len(train_dataframe.select_dtypes(include=["number"]).columns) > 0:
                print("Numerical columns exist")

            #chech datadrift

        except Exception as e:
            raise NetworkSecurityException(e,sys)