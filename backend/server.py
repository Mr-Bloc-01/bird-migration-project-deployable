import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import pandas as pd
from inference_sdk import InferenceHTTPClient
from PIL import Image
import os
import pickle

from firebase_options import update_document

app = Flask(__name__)  # Creating the 'app' as a server

CORS(app, supports_credentials=True, resources={r"/*": {
    "origins": "*",
    "allow_headers": ["Content-Type"],
    "methods": ["GET", "POST", "OPTIONS"]
}}, automatic_options=True)   # enable CORS for the flask server

# Load the models once when the application starts
with open('DT_Model_Latitude.pkl', 'rb') as file:
    latitude_model = pickle.load(file)

with open('DT_Model_Longitude.pkl', 'rb') as file:
    longitude_model = pickle.load(file)

# Load the dataset with daily temperature, wind speed, and wind direction
data = pd.read_csv('bird_migration_temp_andwind_speed.csv')

def predict_migration(change_in_temperature, change_in_wind_speed):
    # Helper function to predict migration for each day of the year using the preloaded model.

    # Remove leading and trailing whitespaces from column names
    data.columns = data.columns.str.strip()

    # Remove leading and trailing whitespaces from each cell
    for col in data.columns:
        if pd.api.types.is_string_dtype(data[col]):
            data[col] = data[col].str.strip()

    predictions = []
    for _, row in data.iterrows():
        # Extract relevant data from the dataset
        month = row['month']
        day = row['day']
        
        # Apply the user-inputted changes to temperature and wind speed
        adjusted_temperature = row['temperature'] + change_in_temperature
        adjusted_wind_speed = row['wind_speed'] + change_in_wind_speed

        print(row['temperature'])
        print(row['wind_speed'])

        print("change in temp:       " + str(change_in_temperature))
        print("change in wind speed: " + str(change_in_wind_speed))
        
        # Prepare the input for the model
        # Make sure this matches the model input format
        processed_data = np.array([[month, day, adjusted_temperature, adjusted_wind_speed]])
        
        # Make a prediction
        longitude_prediction = longitude_model.predict(processed_data)
        latitude_prediction = latitude_model.predict(processed_data)
        
        # Extract the predicted longitude and latitude
        pred_latitude = latitude_prediction[0]
        pred_longitude = longitude_prediction[0]
        
        # Format the prediction result
        prediction_result = f"{month}/{day}/{pred_longitude:.2f}/{pred_latitude:.2f}"
        predictions.append(prediction_result)
    
    return predictions


def predict_bird(bird_image_path):  # open bird image and predict what bird is found
    CLIENT = InferenceHTTPClient(
        api_url="https://classify.roboflow.com",
        api_key="sDnLswHc5x8Cc9J9bS8u"
    )

    try:
        result = CLIENT.infer(bird_image_path, model_id="bird-species-detector/851")
    except Exception:
        return 'nothing', 0
    

    predictions = result['predictions']
    predicted_class = predictions[0]['class']
    confidence = predictions[0]['confidence']

    return predicted_class, confidence  # return the prediction and confidence


@app.route("/")
def main_route():
    return "Hello World!"

# route for migration prediction
@app.route("/migration_prediction", methods=['POST'])
def get_prediction():

    if not request.is_json:
        return jsonify({'error': 'No JSON data received'}), 400
    
    json_data = request.get_json()

    change_in_temp = json_data["change_in_temp"]
    change_in_wind_speed = json_data["change_in_wind_speed"]

    print(change_in_temp)
    print(change_in_wind_speed)

    # Get user inputs from query parameters
    # change_in_temp = float(request.args.get('change_in_temperature', 0))
    # change_in_wind_speed = float(request.args.get('change_in_wind_speed', 0))
    
    # Call the helper function to get predictions for all days
    prediction_results = predict_migration(change_in_temp, change_in_wind_speed)
    
    # Return predictions as a JSON response
    return jsonify({'predictions': prediction_results})


# route to determine bird species based on sent image
@app.route("/bird_detection", methods=["POST"])
def bird_detection():

    if 'file' not in request.files:
        return jsonify({'error': 'No file sent over dude.'})
    
    file = request.files['file']
    
    if file.filename == "":
        return jsonify({"error": "No file selected."})
    
    image = Image.open(file.stream)
    image.save("tmp_bird_image.png")

    predicted_class, confidence = predict_bird("tmp_bird_image.png")

    return jsonify({'class': predicted_class, "confidence": confidence})


# route for users to upload their own sighting data
@app.route("/upload-data", methods=["POST"])
def upload_data():
    if not request.is_json:
        return jsonify({'error': 'No JSON data received'}), 400
    
    json_data = request.get_json()

    species = json_data["species"]
    temperature = json_data["temperature"]
    wind_speed = json_data["wind_speed"]
    direction = json_data["wind_direction"]
    coords = json_data["coords"]

    field_name = "user_input_" + str(datetime.datetime.now())   # ensure the field name is unique by adding the time

    # call the update_document function
    update_document(
        "user_submitted_data",
        str(datetime.date.today().year),
        field_name,
        {
            "species": species,
            "temperature": temperature,
            "wind_speed": wind_speed,
            "wind_direction": direction,
            "coords": coords
        }
    )

    return jsonify({"response": "Successfully added data to database."})


# Main will actually run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    #predict_migration(2, 0)
    # predictions, predicted_class, confidence = predict_bird("blue-jay.jpeg")
    # print(predict_bird)
