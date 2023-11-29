import json
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import recall_score, precision_score, f1_score 

def train_classifier(dataset):

  # Extract features and labels from the dataset
  features = []
  labels = []

  for entry in dataset:
    for key, value in entry.items():
      features.append({"crop_index": int(value[0]), "month": int(value[1])})
      labels.append(int(key))

  # Print the dataset before feeding it to the AI model
  # print("Dataset:")
  # for i in range(len(labels)):
    # print(f"Label: {labels[i]}, Features: {features[i]}")


  # Convert features to a sparse matrix
  global vectorizer
  vectorizer = DictVectorizer(sparse=False)
  features_matrix = vectorizer.fit_transform(features)

  # Split the data into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(features_matrix, labels, test_size=0.2, random_state=42)

  # print("=========")
  # print(X_train)
  # print(y_train)
  # print("=========")

  # Create and train the Multinomial Naive Bayes classifier
  clf = MultinomialNB()
  clf.fit(X_train, y_train)

  # Make predictions on the test set
  y_pred = clf.predict(X_test)

  # Evaluate accuracy
  accuracy = accuracy_score(y_test, y_pred)
  # print(f"Accuracy on the test set: {accuracy}")

  # Calculate additional metrics
  precision = precision_score(y_test, y_pred)
  recall = recall_score(y_test, y_pred)
  f1 = f1_score(y_test, y_pred)

  # print(f"Precision: {precision}")
  # print(f"Recall: {recall}")
  # print(f"F1 Score: {f1}")

  conf_mat = confusion_matrix(y_test, y_pred, labels=[0, 1])
  # print("Confusion Matrix:")
  # print(conf_mat)

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
  }

  try:
    model = classifier_model
    user_crop_index = int(inputs['crop'])
    user_month = int(inputs['month'])

    # Transform user input into the format expected by the model
    user_input = [{"crop_index": user_crop_index, "month": user_month}]
    user_input_matrix = vectorizer.transform(user_input)

    # Make predictions on user input
    user_prediction = model.predict(user_input_matrix)

    output = f"The classification output for {crops[user_crop_index]} crops, in conjunction with the harvest expectations for {months[user_month]}, is predicted to result in a {'POSITIVE return on investment' if user_prediction[0] == 1 else 'NEGATIVE return on investment'}."
    return output

  except:
    output = "ERROR: Classification failed."
    return output