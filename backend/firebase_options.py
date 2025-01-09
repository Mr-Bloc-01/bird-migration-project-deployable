import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import pandas as pd

cred = credentials.Certificate("birdMigrationServiceAccountKey.json")
firebase_admin.initialize_app(cred)

# initialize the client to firestore
db = firestore.client()

# function to update documents 
def update_document(collection_name, document_id, field_name, field_value):
    try:
        # initialize the reference to the document to create/update
        doc_ref = db.collection(collection_name).document(document_id)  

        # update or create data in the document 
        doc_ref.set({field_name: field_value}, merge=True)

        print(f"The {document_id} document has been updated with the data: {field_value}")
    except Exception as error :
        print(f"Error: {error}")


# function to create a csv file with the data from the database
def create_dataset(year, species, file_name):
    # create empty data columns
    columns = {
        [],
        [],
    }

    # initialize the dataframe
    df = pd.DataFrame(columns)

    # initialize the document reference
    doc_ref = db.collection("user_submitted_data").document(year)

    # get snapshot
    snapshot = doc_ref.get()

    for item in snapshot:
        if (item["species"] == species):
            # add items from snapshot to dataframe
            df["species"] = item["species"]
            df["temperature"] = item["temperature"]
            df["wind_speed"] = item["wind_speed"]
            df["wind_direction"] = item["wind_direction"]
            df["coords"] = item["coords"]

    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    field_name = "user_input_" + str(datetime.datetime.now())   # ensure the field name is unique by adding the time

    # call the update_document function
    update_document(
        "user_submitted_data",
        str(datetime.date.today().year),
        field_name,
        {
            "species": "Blue Jay",
            "temperature": 24.0,
            "wind_speed": 2.0,
            "flight_direction": "N",
            "coords": [0, 0]
        }
    )