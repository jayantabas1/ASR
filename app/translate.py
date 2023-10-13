# app/routes.py

import os
import replicate
from flask import render_template, request, jsonify, Flask,Blueprint
from app import app
from dotenv import load_dotenv
import time
import uuid
import datetime
import concurrent.futures

# Load environment variables from .env file
# os.environ["REPLICATE_API_TOKEN"] = "your_api_token_here"
load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")

# Set your Replicate API token from your environment variable
# replicate_api_token = os.getenv("REPLICATE_API_TOKEN")

UPLOADED_FOLDER = 'D:\\seamless-flask-app\\seamlessm4t-app\\recordings'

upload_route_blueprint = Blueprint("upload", __name__)

@upload_route_blueprint.route('/upload', methods=['POST'])
def upload():
    print("Receiving translation request")
    audio_file = request.files['audio']
    # Generate a unique filename using a UUID
    unique_filename = str(uuid.uuid4()) + '.wav'
    filepath = os.path.join(UPLOADED_FOLDER, unique_filename)
    audio_file.save(filepath)
    transcription_1 = ""
    transcription_2 = ""

    # Use Replicate to perform speech-to-speech translation to english
    start_time = datetime.datetime.now()
    print("first call")
    def translate_to_english():
        if replicate_api_token:
            try:
                f = open(filepath, "rb")
                output_english = replicate.run(
                    "cjwbw/seamless_communication:668a4fec05a887143e5fe8d45df25ec4c794dd43169b9a11562309b2d45873b0",
                    input={"task_name": "S2TT (Speech to Text translation)", "input_audio": f, "target_language_text_only": "English"}
                )
                print("call complete")
                transcription_1 = output_english["text_output"]
            except Exception as e:
                print("Error in Replicate translation (English):", str(e))
                transcription_1 = "Translation error"
        else:
            transcription_1 = "Replicate API token not set"
        return transcription_1

# Use Replicate to perform speech-to-text translation for Assamese
    print("second call")
    def translate_to_assamese():
        if replicate_api_token:
            try:
                print ("inside try block, calling API")
                f = open(filepath, "rb")
                output_assamese = replicate.run(
                    "cjwbw/seamless_communication:668a4fec05a887143e5fe8d45df25ec4c794dd43169b9a11562309b2d45873b0",
                    input={"task_name": "S2TT (Speech to Text translation)", "input_audio": f, "target_language_text_only": "Assamese"}
                )
                print("call complete")
                transcription_2 = output_assamese["text_output"]
            except Exception as e:
                print("Error in Replicate translation (Assamese):", str(e))
                transcription_2 = "Translation error"
        else:
            transcription_2 = "Replicate API token not set"
        return transcription_2
    
    # Use concurrent.futures to run translations concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(translate_to_english)
        future2 = executor.submit(translate_to_assamese)

        # Wait for both translations to complete
        concurrent.futures.wait([future1, future2])

        # Get the results of the translations
        transcription_1 = future1.result()
        transcription_2 = future2.result()

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print("total time taken", elapsed_time)
        
    return jsonify({'translation1': transcription_1, 'translation2': transcription_2})
    # return jsonify({'transcription2': transcription_2})
