import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os

class MaternalDataPreprocessor:
    def __init__(self):
        self.column_transformer = None
        self.target_column = 'MMO'
        
    def get_feature_types(self, df):
        """
        Identifies numerical and categorical columns.
        """
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if self.target_column in numerical_cols:
            numerical_cols.remove(self.target_column)
            
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        return numerical_cols, categorical_cols

    def build_pipeline(self, df):
        """
        Builds a preprocessing pipeline with imputation, scaling, and encoding.
        """
        num_cols, cat_cols = self.get_feature_types(df)
        
        # Numerical pipeline: Impute missing with median -> StandardScale
        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # Categorical pipeline: Impute missing with most frequent -> OneHotEncode
        cat_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        self.column_transformer = ColumnTransformer([
            ('num', num_pipeline, num_cols),
            ('cat', cat_pipeline, cat_cols)
        ])
        
        return self.column_transformer

    def fit_transform(self, df):
        """
        Fits the pipeline to the data and transforms it.
        """
        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]
        
        if self.column_transformer is None:
            self.build_pipeline(df)
            
        X_processed = self.column_transformer.fit_transform(X)
        return X_processed, y

    def transform(self, df):
        """
        Transforms new data using the fitted pipeline.
        """
        if self.column_transformer is None:
            raise ValueError("Preprocessor has not been fitted yet.")
            
        X = df.drop(columns=[self.target_column]) if self.target_column in df.columns else df
        return self.column_transformer.transform(X)

    def save_artifacts(self, path="models/"):
        """
        Saves the preprocessor artifacts.
        """
        os.makedirs(path, exist_ok=True)
        joblib.dump(self.column_transformer, os.path.join(path, "preprocessor.pkl"))
        print(f"Preprocessor artifacts saved to {path}")

    def load_artifacts(self, path="models/preprocessor.pkl"):
        """
        Loads preprocessor artifacts.
        """
        self.column_transformer = joblib.load(path)
        print(f"Preprocessor artifacts loaded from {path}")

if __name__ == "__main__":
    # Local test with synthetic data
    try:
        data_path = "data/raw/synthetic_masha_data.csv"
        df = pd.read_csv(data_path)
        
        preprocessor = MaternalDataPreprocessor()
        X_processed, y = preprocessor.fit_transform(df)
        
        print("Original shape:", df.shape)
        print("Processed shape:", X_processed.shape)
        print("Preprocessing successful.")
    except ImportError:
        print("Pandas/Scikit-learn not installed. Code is ready for Colab.")
    except Exception as e:
        print(f"Error: {e}")
