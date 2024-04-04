import json
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import recall_score, precision_score, f1_score, classification_report
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tqdm import tqdm
import time

import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime

def train_classifier(dataset):

  # Extract features and labels from the dataset
  features = []
  labels = []

  for entry in dataset:
    for key, value in entry.items():
      features.append({"crop_index": int(value[0]), "month": int(value[1])})
      labels.append(int(key))

  # Convert features to a sparse matrix
  global vectorizer
  vectorizer = DictVectorizer(sparse=False)
  features_matrix = vectorizer.fit_transform(features)

  # Split the data into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(features_matrix, labels, test_size=0.2, random_state=42)
  # Create and train the Multinomial Naive Bayes classifier
  clf = MultinomialNB()
  clf.fit(X_train, y_train)

  # Make predictions on the test set
  y_pred = clf.predict(X_test)

  # Evaluate accuracy
  accuracy = accuracy_score(y_test, y_pred)

  # Calculate additional metrics
  precision = precision_score(y_test, y_pred)
  recall = recall_score(y_test, y_pred)
  f1 = f1_score(y_test, y_pred)
  conf_mat = confusion_matrix(y_test, y_pred, labels=[0, 1])

  global classifier_model
  classifier_model = clf
  
  output = {
    'accuracy': str(round(accuracy, 4) * 100) + '%',
    'precision': str(round(precision, 4) * 100) + '%',
    'recall': str(round(recall, 4) * 100) + '%',
    'f1_score': str(round(f1, 4) * 100) + '%',
    'confusion_mat': str(conf_mat),
  }

  return output

def classify(inputs):

  months = {
    0: "January",
    1: "February",
    2: "March",
    3: "April",
    4: "May",
    5: "June",
    6: "July",
    7: "August",
    8: "September",
    9: "October", 
    10: "November",
    11: "December",
  }

  crops = {
    0: "Mango",
    1: "Sugarcane",
    2: "Banana",
    3: "Coconut",
    4: "Cabbage",
    5: "Eggplant",
    6: "Mongo",
    7: "Tomato",
  }

  result_string = ''

  try:
    model = classifier_model
    start_time = time.time()

    with tqdm(total=1, desc="Classification progress", position=0, leave=True) as pbar:
      user_crop_index = int(inputs['crop'])
      user_month = int(inputs['month'])

      # Transform user input into the format expected by the model
      user_input = [{"crop_index": user_crop_index, "month": user_month}]
      user_input_matrix = vectorizer.transform(user_input)
      
      # Make predictions and get probability estimates
      user_prediction_prob = model.predict_proba(user_input_matrix)
      user_prediction = model.predict(user_input_matrix)

      # Get the class index with the highest probability
      predicted_class_index = np.argmax(user_prediction_prob)

      # Get the confidence score for the predicted class
      confidence_score = user_prediction_prob[0, predicted_class_index]

      # Convert the confidence score to percentage
      confidence_percentage = round(confidence_score * 100, 2)

      # Build the result string
      result_string = f"\nMultinomial Naive Bayes Classification:\nprediction: {user_prediction}\nprediction_prob: {user_prediction_prob[0]}"

      output = f"The classification output for {crops[user_crop_index]} crops, for the month of {months[user_month]}, is predicted to result in a {'POSITIVE return on investment' if predicted_class_index == 1 else 'NEGATIVE return on investment'}.\n AI Accuracy Confidence: {confidence_percentage}%.\n Improvement of the dataset may increase AI scores and accuracy."

      pbar.update(1)

      elapsed_time = time.time() - start_time
      progress_rate = pbar.n / elapsed_time if elapsed_time > 0 else 0
      result_string += f"\nElapsed Time: {elapsed_time * 1000:.2f} milliseconds"
      result_string += f"\nElapsed Time: {elapsed_time * 1e6:.2f} microseconds"
      result_string += f"Progress Rate: {progress_rate:.2f} iterations/second\n"
      result_string += f"Classification progress: 100%|================================|1/1 [{progress_rate:.2f} it/s]"
      
    return output, result_string
  except:
    output = ""
    return output, result_string 
  
def get_dataset_linear_regression(data):

  crop_data = {}
  for index, row in data.iterrows():
    # print(row)
    crop = row['CROP']
    row_data = {
      "Q1": [row['Q1']],
      "Q2": [row['Q2']],
      "Q3": [row['Q3']],
      "Q4": [row['Q4']],
      "Q1.1": [row['Q1.1']],
      "Q2.1": [row['Q2.1']],
      "Q3.1": [row['Q3.1']],
      "Q4.1": 0
    }
    df = pd.DataFrame(row_data)
    df.fillna(df.mean(), inplace=True)
    crop_data[crop] = df

  return crop_data

def train_classifier2(crop_data):
  models = {}
  scores = {}

  for crop, df in crop_data.items():
    X = np.arange(1, len(df.columns) + 1).reshape(-1, 1)
    y = df.values.flatten()
    model = LinearRegression()
    model.fit(X, y)
    models[crop] = model

    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)
    scores[crop] = {'MAE': round(mae, 4), 'MSE': round(mse, 4), 'RMSE': round(rmse, 4), 'R_squared': round(r2, 4)}

  global classifier_2_models
  classifier_2_models = models

  global classifier_2_scores
  classifier_2_scores = scores

  return models, scores

def classify2(initial_investment, harvest_month, harvest_year, crop):
  model = classifier_2_models[crop]
  model_score = classifier_2_scores[crop]
  
  initial_investment = float(initial_investment)
  harvest_month = int(harvest_month)
  harvest_year = int(harvest_year)

  # Calculate the quarter index for the harvest month and year
  harvest_date = datetime(int(harvest_year), int(harvest_month), 1)
  quarter_index = (harvest_date.month - 1) // 3
  
  # Predict the farmgate price increase
  predicted_increase = model.predict([[quarter_index + 1]])
  
  # Calculate ROI
  total_return = initial_investment * (predicted_increase / 100)
  roi = (total_return / initial_investment) * 100
  
  return roi[0], total_return, model_score