import os
import pandas as pd
from housing_pricer.config.configuration import ConfigurationManager
from housing_pricer.entity.config_entity import DataTransformationConfig
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.target_column = self.config.target_column

    def clean_and_engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        print("--- Starting manual data cleaning & feature engineering ---")
        df_cleaned = df.dropna(subset=[self.target_column]).copy()

        if 'Address' in df.columns:
            df_cleaned = df_cleaned.drop('Address', axis=1)

        if 'Date' in df_cleaned.columns:
            df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], format='%d/%m/%Y')
            df_cleaned['Sale_Year'] = df_cleaned['Date'].dt.year
            df_cleaned['Sale_Month'] = df_cleaned['Date'].dt.month
            df_cleaned = df_cleaned.drop('Date', axis=1)
            
        price_cap = df_cleaned[self.target_column].quantile(0.99)
        df_cleaned = df_cleaned[df_cleaned[self.target_column] < price_cap]

        suburb_counts = df_cleaned['Suburb'].value_counts()
        rare_suburbs = suburb_counts[suburb_counts < 100].index
        df_cleaned['Suburb'] = df_cleaned['Suburb'].replace(rare_suburbs, 'Other')

        council_counts = df_cleaned['CouncilArea'].value_counts()
        rare_councils = council_counts[council_counts < 100].index
        df_cleaned['CouncilArea'] = df_cleaned['CouncilArea'].replace(rare_councils, 'Other')

        
        seller_counts = df_cleaned['SellerG'].value_counts()
        rare_sellers = seller_counts[seller_counts < 100].index
        df_cleaned['SellerG'] = df_cleaned['SellerG'].replace(rare_sellers, 'Other')

        print(f"Data cleaned. New shape: {df_cleaned.shape}")

        return df_cleaned

    def get_preprocessor_object(self):
        print("--- Building preprocessor object ---")
        numeric_features = ['Rooms', 'Distance', 'Propertycount', 'Sale_Year', 'Sale_Month']

        num_pipeline = Pipeline(steps=[
            
            ('imputer', SimpleImputer(strategy='median')),
            
            ('scaler', StandardScaler())
        ])

        categorical_features = ['Suburb', 'Type', 'Method', 'SellerG', 'Regionname', 'CouncilArea', 'Postcode']

        cat_pipeline = Pipeline(steps=[
            
            ('imputer', SimpleImputer(strategy='most_frequent')),
            
            ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore')),
            
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num_pipeline', num_pipeline, numeric_features),
                ('cat_pipeline', cat_pipeline, categorical_features)
            ],
            remainder='passthrough')

        print("--- Preprocessor object built ---")
        return preprocessor

    def run_transformation(self):
        print("--- Starting Data Transformation Component ---")
        try:
            os.makedirs(self.config.root_dir, exist_ok=True)
            df = pd.read_csv(self.config.data_to_transform)
            df_clean = self.clean_and_engineer_features(df)

            print("Splitting data into train and test sets...")
            train_df, test_df = train_test_split(df_clean, test_size=0.2, random_state=42)
            train_df.to_csv(self.config.train_data_path, index=False)
            test_df.to_csv(self.config.test_data_path, index=False)
            print(f"Train.csv and Test.csv saved to: {self.config.root_dir}")

            preprocessor = self.get_preprocessor_object()
            train_features = train_df.drop(self.target_column, axis=1)
            preprocessor.fit(train_features)

            joblib.dump(preprocessor, self.config.preprocessor_obj_file)
            print(f"Preprocessor object saved to: {self.config.preprocessor_obj_file}")
            
            print("--- Data Transformation Component Complete ---")

        except Exception as e:
            print(f"Error during data transformation: {e}")
            raise e



    
        
        







