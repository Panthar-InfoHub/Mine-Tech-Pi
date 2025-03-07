from google import genai
from google.genai import types
import logging
import json

model_name= "gemini-2.0-flash-lite-001"
project_name = "suraksha-kawach-151024"
project_location="asia-south1"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('suraksha.ai')

client = genai.Client(
    vertexai=True,
    project='suraksha-kawach-151024',
    location='us-central1',
    http_options={'api_version': 'v1'}
)

intro = (
    "Welcome to the Mining Resource Security AI Analyzer. This system is designed to process "
    "video or image footage of vehicles approaching or leaving ore mine sites. The primary objective "
    "is to identify vehicles, particularly trucks and heavy load carrying vehicles, and perform a "
    "detailed analysis to verify if they are transporting any materials that might be subject to royalty "
    "fees. If a vehicle is identified as a truck or heavy load carrier, further analysis will be performed "
    "to determine whether it contains any cargo. The results of the analysis will be returned in a structured "
    "JSON format including identifiers such as the vehicle number, flags (e.g., whether a number was found), "
    "and confidence scores for each detection step. Please ensure that the footage provided is clear and meets "
    "the required quality standards for best results."
)


identify_vehicle_instructions = (
    "The system receives video or image data and returns vehicle analysis results in JSON format. The JSON "
    "object must contain the following detailed fields:"
    "• vehicle_number: A string representing the unique identifier of the vehicle (e.g., license plate number)."
    "• is_number_found: A boolean flag indicating whether a vehicle number was successfully detected."
    "• vehicle_type: A string that specifies the type of the vehicle (e.g., 'Truck', 'Heavy Load', 'Other')."
    "• is_carrying_contents: A boolean flag that indicates if the vehicle is carrying any contents."
    "• contents_details: If contents are detected, include an object with further details about the contents. "
    "This may include categories or identifiers for the type of cargo."
    "• confidence_scores: An object containing numerical values (typically between 0.0 and 1.0) representing "
    "the confidence of each determined classification. For example:"
    "    • vehicle_classification: Confidence score for the vehicle type detected."
    "    • cargo_detection: Confidence score for the detection of any cargo."
    "    • number_recognition: Confidence score for the vehicle number detection."
    "Ensure that your data format is strictly adhered to in order to facilitate efficient and accurate processing."
) + "\n\n" + intro


def analyze_video(bucket_urls: list[str], is_video: bool = True):
    try:
        generated_analysis = client.models.generate_content(
            model=model_name,
            contents=[
                # instruction 1
                types.Part(
                    text=(
                        "Firstly check if the video is fake or AI Generated or 3D generated."
                        "if it's not fake, then analyze the video contents in detail, focusing on identifying the vehicle's number, make, model and if it's carrying any contents "
                        "It is very important that you identify that if the vehicle is a heavy vehicle i.e. truck, bus, etc. and if it's carrying any contents. "
                        "You primary focus should be on trucks. Trucks must be analyzed thoroughly"
                    )
                ),
                # Content identification
                types.Part(
                    text=f"After identification of the vehicle, you need to identify if it is carrying any contents."
                         f" If it is carrying any contents, then you need to analyze the contents."
                         f"Your focus on should be identifying if contents belong to mining. This means coal, ore, "
                         f"minerals, etc. Based on the generation config provided to your populated"
                         f"the correct fields"
                ),
                # images file data
                [types.Part(
                    file_data=types.FileData(
                        file_uri=bucket_url,

                        mime_type="video/mp4" if is_video else "image/jpeg"
                    )
                ) for bucket_url in bucket_urls]
            ],
            config=types.GenerateContentConfig(
                max_output_tokens=5000,
                response_mime_type="application/json",
                system_instruction=json.dumps(identify_vehicle_instructions)
            )
        )

        return generated_analysis.text
    except Exception as e:
        logger.error(f"Failed to analyze video with bucket_url: {bucket_urls}", exc_info=True)
        return {"error": "Failed to analyze video", "details": str(e)}
