import pandas as pd
import numpy as np
from field_data_processor import FieldDataProcessor

config_params = {
    "sql_query": """
            SELECT *
            FROM geographic_features
            LEFT JOIN weather_features USING (Field_ID)
            LEFT JOIN soil_and_crop_features USING (Field_ID)
            LEFT JOIN farm_management_features USING (Field_ID)
            """,
    "db_path": 'sqlite:///Maji_Ndogo_farm_survey_small.db',
    "columns_to_rename": {'Annual_yield': 'Crop_type', 'Crop_type': 'Annual_yield'},
    "values_to_rename": {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'},
    "weather_csv_path": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv",
    "weather_mapping_csv": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv",
    "regex_patterns" : {
            'Rainfall': r'(\d+(\.\d+)?)\s?mm',
            'Temperature': r'(\d+(\.\d+)?)\s?C',
            'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
            },
}

field_processor = FieldDataProcessor(config_params)
field_processor.process()
field_df = field_processor.df
dataset = field_df.drop("Weather_station", axis=1)
dataset_enc = dataset.drop('Field_ID', axis=1)
dataset_enc = pd.get_dummies(dataset_enc, drop_first=True)

target = 'Standard_yield'
options = ['Pollution_level', 'Crop_type_tea', 'Annual_yield', 'Longitude']

print("Correlations with Standard_yield:")
for opt in options:
    if opt in dataset_enc.columns:
        corr = dataset_enc[opt].corr(dataset_enc[target])
        print(f"{opt}: {corr}")
    else:
        print(f"{opt} not in columns")
