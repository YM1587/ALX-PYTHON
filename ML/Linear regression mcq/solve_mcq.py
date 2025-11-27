import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from field_data_processor import FieldDataProcessor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Config params from notebook
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

print("--- Loading Data ---")
field_processor = FieldDataProcessor(config_params)
field_processor.process()
field_df = field_processor.df
dataset = field_df.drop("Weather_station", axis=1)

print("\n--- Question 1 ---")
# How many predictors do we originally have in our dataset, and which of these are categorical in nature?
# Exclude Field_ID and Standard_yield (target)
predictors = [c for c in dataset.columns if c not in ['Field_ID', 'Standard_yield']]
print(f"Number of predictors: {len(predictors)}")
categorical = dataset[predictors].select_dtypes(include=['object', 'category']).columns.tolist()
print(f"Categorical predictors: {categorical}")
print(f"All columns: {dataset.columns.tolist()}")

print("\n--- Question 2 ---")
# Dummy variable encoding
# Exclude Field_ID
dataset_enc = dataset.drop('Field_ID', axis=1)
dataset_enc = pd.get_dummies(dataset_enc, drop_first=True)
# How many independent variables? (Exclude Standard_yield)
indep_vars = [c for c in dataset_enc.columns if c != 'Standard_yield']
print(f"Number of independent variables after encoding: {len(indep_vars)}")

print("\n--- Question 3 ---")
# Correlation with Standard_yield
corr = dataset_enc.corr()['Standard_yield'].abs().sort_values(ascending=False)
print("Top correlations with Standard_yield (abs):")
print(corr.head(10))

print("\n--- Question 5 ---")
# Fit OLS and check p-values
# Ensure all boolean are int (get_dummies does this usually, but let's be safe)
dataset_enc = dataset_enc.astype(float)
X = dataset_enc.drop('Standard_yield', axis=1)
y = dataset_enc['Standard_yield']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print("Significant variables (p < 0.05):")
p_values = model.pvalues
sig_vars = p_values[p_values < 0.05].index.tolist()
print(sig_vars)
# Check specific options
options = ['Slope', 'Elevation', 'pH', 'Soil_fertility']
for opt in options:
    if opt in p_values:
        print(f"{opt}: p-value = {p_values[opt]}")

print("\n--- Question 6 ---")
# Correlation matrix heatmap (we'll just check values)
# Check pairs:
pairs = [
    ('Plot_size', 'Crop_type_tea'),
    ('Pollution_level', 'Soil_type_Rocky'), # Note: Soil_type_Rocky might be Soil_type_Rocky (dummy)
    ('Crop_type_cassava', 'Soil_type_Sandy'),
    ('Min_temperature_C', 'Elevation')
]

# Check if columns exist
cols = dataset_enc.columns
for p1, p2 in pairs:
    if p1 in cols and p2 in cols:
        c = dataset_enc[p1].corr(dataset_enc[p2])
        print(f"Correlation between {p1} and {p2}: {c}")
    else:
        print(f"Columns not found for pair {p1}, {p2}")

print("\n--- Question 7 ---")
print(model.summary())

print("\n--- Question 8 ---")
# Reduced model
vars_reduced = [
    'Pollution_level', 
    'Crop_type_coffee', 
    'Crop_type_tea', 
    'Location_Rural_Sokoto', 
    'Annual_yield', 
    'Soil_type_Silt', 
    'Soil_type_Volcanic'
]
# Check if these exist
valid_vars = [v for v in vars_reduced if v in dataset_enc.columns]
if len(valid_vars) != len(vars_reduced):
    print(f"Missing vars: {set(vars_reduced) - set(valid_vars)}")

X_red = dataset_enc[valid_vars]
X_red = sm.add_constant(X_red)
model_red = sm.OLS(y, X_red).fit()
print("Reduced Model Summary:")
print(model_red.summary())
print(f"Full Model AIC: {model.aic}, R-squared: {model.rsquared}")
print(f"Reduced Model AIC: {model_red.aic}, R-squared: {model_red.rsquared}")

print("\n--- Question 9 ---")
# Residuals vs Fitted
# We can't plot, but we can check properties?
# "What does the scatter plot tell us?"
# Usually we look for patterns.
# I'll just print that I can't see the plot but I can check for homoscedasticity using a test if needed.
# Breusch-Pagan test
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(model.resid, model.model.exog)
print(f"Breusch-Pagan test p-value: {bp_test[1]}")

