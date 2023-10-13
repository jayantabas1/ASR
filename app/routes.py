# app/routes.py

import os
import replicate
from flask import render_template, request, jsonify, Flask,Blueprint
from app import app

# Set your Replicate API token from your environment variable
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")

home_route_blueprint = Blueprint("home", __name__)

@home_route_blueprint.route('/')
def home():
    return render_template("index.html")

# @app.route('/upload', methods=['POST'])
# def upload():
#     # Handle the uploaded audio file here and perform transcription
#     audio_file = request.files['audio']

#     # Implement your speech-to-text logic here using a library or API
#     # Replace the following mock results with actual transcription results
#     transcription_1 = ""
#     transcription_2 = ""

#     # Use Replicate to perform speech-to-speech translation
#     if replicate_api_token:
#         try:
#             output_english = replicate.run(
#                 "cjwbw/seamless_communication:668a4fec05a887143e5fe8d45df25ec4c794dd43169b9a11562309b2d45873b0",
#                 input={"task_name": "S2TT (Speech to Text translation)", "input_audio": audio_file, "target_language_text_only": "English"}
#             )
#             transcription_1 = output_english["text_output"]
#         except Exception as e:
#             print("Error in Replicate translation (English):", str(e))
#             transcription_1 = "Translation error"
#     else:
#         transcription_1 = "Replicate API token not set"

# # Use Replicate to perform speech-to-text translation for Assamese
#     if replicate_api_token:
#         try:
#             output_assamese = replicate.run(
#                 "cjwbw/seamless_communication:668a4fec05a887143e5fe8d45df25ec4c794dd43169b9a11562309b2d45873b0",
#                 input={"task_name": "S2TT (Speech to Text translation)", "input_audio": audio_file, "target_language_text_only": "Assamese"}
#             )
#             transcription_2 = output_assamese["text_output"]
#         except Exception as e:
#             print("Error in Replicate translation (Assamese):", str(e))
#             transcription_2 = "Translation error"
#     else:
#         transcription_2 = "Replicate API token not set"
#         # You can perform a similar translation for transcription_2 if needed

#     # Return the transcription and translation results as JSON
#     return jsonify({'transcription1': transcription_1, 'transcription2': transcription_2})
