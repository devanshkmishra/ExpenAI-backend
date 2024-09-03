from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os
from PIL import Image
import io
import google.generativeai as genai
import json
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import shutil
import assemblyai as aai

# Load environment variables
load_dotenv()

aai.settings.api_key = os.getenv("AAI_API_KEY")
# Configure the generative AI library
# This is a placeholder for actual configuration
# Replace with actual configuration code

# Initialize the FastAPI app
app = FastAPI()

# Placeholder for the generative model configuration
# This should be replaced with actual code to configure the model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel(model_name='gemini-pro-vision')
model2 = genai.GenerativeModel(model_name='gemini-pro')


def get_gemini_response(input, image):
    response = model.generate_content([input, image[0]])
    return response.text

async def input_image_details(uploaded_file: UploadFile):
    if uploaded_file is not None:
        # Read the file content into bytes
        bytes_data = await uploaded_file.read()

        image_parts = [
            {
                "mime_type": uploaded_file.content_type, # Use content_type instead of type
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response_text(prompt, input=None):
    content = [input, prompt]
    response = model2.generate_content(content)

    return response.text


input_prompt="""
You are an expert at understanding invoices and managing expenses. I will upload an image of an invoice. You will have to analyze the invoice and return the category and amount of the bill as shown in the following json format. return only this json and nothing else. Ensure that you follow the format exactly as shown below, and parse it correctly as a json file, indent the json by using escape characters as shown in the format below:

{\n"category": "bill category",\n\t"amount": amount in integer\n}

Here category has to be one of the following: "medical, food, travel, entertainment, education, stationery, shopping" and amount in integer has to be the final amount of the invoice. If the final amount is not explicitly mentioned, you have to calculate the amount from the invoice by adding up each object's price. If the category is not clear, choose the most probable category but only out of the ones mentioned.
"""

input_prompt_text="""
You are an expert at understanding invoices and managing expenses. I will give a textual description of my expenses. You will have to understand the expenses and return the category and amount of the bill as shown in the following json format. if there are multiple items, ensure that you add up the price of each item correctly. return only this json and nothing else. Ensure that you follow the format exactly as shown below, and parse it correctly as a json file, indent the json by using escape characters as shown in the format below:

{\n"category": "bill category",\n\t"amount": amount in integer\n}

Here category has to be one of the following: "medical, food, travel, entertainment, education, stationery, shopping" and amount in integer has to be the final amount of the invoice. If the final amount is not explicitly mentioned, you have to calculate the amount from the invoice by adding up each object's price. For example, if the input is "5 pens for 10 rupees each and 3 notebooks for 30 rupees each", then the calculation will be 5 pens * 10 rupees = 50 rupees for pens and 3 notebooks * 30 rupees = 90 rupees for notebooks. So the total amount in this example will be 50 rupees + 90 rupees = 140 rupees. Wherever there is "and" in the input it usually signifies addition of amounts. Only return category from one of these categories, not anything else. If the category is not clear, choose the most probable category but only out of the ones mentioned.
"""

UPLOAD_DIRECTORY = "uploads"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

transcriber = aai.Transcriber()


def transcribe_wav(file_path):
    try:
        # Transcribe the WAV file
        transcript = transcriber.transcribe(file_path)
        return transcript.text
    except Exception as e:
        return str(e)
    
@app.post("/audio/")
async def upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is a WAV file
    if not file.filename.endswith(".wav"):
        return JSONResponse(status_code=400, content={"error": "Only WAV files are allowed."})

    try:
        # Save the uploaded file
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get the local path of the uploaded file
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        
        # Transcribe the uploaded WAV file
        transcribed_text = transcribe_wav(file_path)
        data_string = get_gemini_response_text(input_prompt_text, transcribed_text)
        json_start = data_string.find('{')
        json_end = data_string.rfind('}')
        json_string = data_string[json_start:json_end+1]
        response = json.loads(json_string)


        return response
        #return {"transcribed_text": transcribed_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/uploadphoto/")
async def upload_photo(file: UploadFile = File(...)):
    if file is not None:
        # Correctly call input_image_details with the UploadFile object
        image_data = await input_image_details(file)
        data_string = get_gemini_response(input_prompt, image_data)
        # Extract the JSON string from the data
        json_start = data_string.find('{')
        json_end = data_string.rfind('}')
        json_string = data_string[json_start:json_end+1]

    # Parse the JSON string
    response = json.loads(json_string)
    # Process the uploaded file here
    return response

class Item(BaseModel):
    prompt: str

@app.post("/prompt/")
def read_item(item: Item):
    data_string = get_gemini_response_text(input_prompt_text, item.prompt)
    json_start = data_string.find('{')
    json_end = data_string.rfind('}')
    json_string = data_string[json_start:json_end+1]
    response = json.loads(json_string)

    return response


