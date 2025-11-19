from dataclasses import dataclass

@dataclass
class DataIngestionArtifcat:
    trained_file_path:str
    test_file_path:str