import sys
from dataclasses import dataclass   
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # ColumnTransformer is used to apply different transformations to different columns of the dataset.
from sklearn.impute import SimpleImputer # SimpleImputer is used to handle missing values in the dataset.
from sklearn.pipeline import Pipeline # Pipeline is used to chain multiple processing steps together.
from sklearn.preprocessing import StandardScaler, OneHotEncoder # StandardScaler is used to standardize numerical features, and OneHotEncoder is used to encode categorical features.
from src.exception import CustomException
from src.logger import logging
import os 
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data trnasformation
        
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)



# Summary of what we’ve done in this step
# Read raw train and test CSVs into pandas DataFrames.
# Get preprocessing object that knows how to handle numerical and categorical columns.
# Separate features and target for both train and test sets.
# Apply transformations:
# Train → fit_transform()
# Test → transform()
# Combine features and target into numpy arrays.
# Save the preprocessing object for future use.
# Return processed train/test arrays and the path of the saved preprocessor.



#fit_transform() and transform() are preprocessing operations
#These methods belong to scikit-learn transformers, not the model itself.
#Scaler → StandardScaler, MinMaxScaler
#Imputer → SimpleImputer
#Encoder → OneHotEncoder, LabelEncoder
#They learn parameters from the data (like mean, std, categories) and apply transformations.

#Fit: Learns statistics from the training data
#Transform: Uses those statistics to transform the training data
#Training data is where the model learns patterns and statistics.

#transform() only Uses the statistics learned from training data

#We must apply the same transformation learned from training data to test/new data,so no fit() on test data.
# Q) Why we transform test data even though it’s “just preprocessing”
# A)Transforming the test data ensures that test features have exactly the same format and scale as training features.
# Q) What would happen if we skip test transformation?
# A) Suppose training data is scaled with StandardScaler.If you feed raw test data to the model:
#    Numerical columns will have completely different scale → model coefficients will not work properly.
#    Predictions will be inaccurate, or some models may throw an error.

#Think of it as “feature alignment”
#Training data → model learns patterns based on scaled & encoded features.
#Test data → must have exactly the same feature representation.
#Transforming test data ensures:
#   i)Same number of columns (especially after one-hot encoding)
#   ii)Same scale for numerical features
#   iii) Same column order