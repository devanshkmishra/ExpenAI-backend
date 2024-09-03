from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
import json
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
import assemblyai as aai

# Load environment variables
load_dotenv()

#aai.settings.api_key = os.getenv("AAI_API_KEY")

# Initialize the FastAPI app
app = FastAPI()

# Configure the Google AI Platform API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
#model2 = genai.GenerativeModel(model_name='gemini-pro')


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
    response = model.generate_content(content)

    return response.text

class InvoiceResponse(BaseModel):
    category: str
    amount: int


input_prompt = """
You are an expert at understanding invoices and managing expenses. I will upload an image of an invoice. You must analyze the invoice image, understand the expenses, and return only the following JSON format:

{\n"category": "bill category",\n\t"amount": amount in integer\n}

Follow these rules:
1. The category must be one of the following: "medical, food, travel, entertainment, education, stationery, shopping".
2. The amount must be the final total from the invoice, calculated by summing up each item's price if necessary.
3. Do not include any text, explanations, or additional information outside of the JSON format.

If you cannot extract the information, return an empty JSON in the same format:

{\n"category": "",\n\t"amount": 0\n}

"""

input_prompt_text = """
You are an expert at understanding invoices and managing expenses. I will give a textual description of my expenses. You will have to understand the expenses, and return only the following JSON format:

{\n"category": "bill category",\n\t"amount": amount in integer\n}

Follow these rules:
1. The category must be one of the following: "medical, food, travel, entertainment, education, stationery, shopping".
2. The amount must be the final total from the invoice, calculated by summing up each item's price if necessary.
3. Do not include any text, explanations, or additional information outside of the JSON format.

If you cannot extract the information, return an empty JSON in the same format:

{\n"category": "",\n\t"amount": 0\n}

"""

UPLOAD_DIRECTORY = "uploads"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    # Read the uploaded audio file into bytes
    audio_bytes = await file.read()

    # Send the audio file and prompt to Gemini
    response = model.generate_content([
        input_prompt_text,
        {
            "mime_type": file.content_type,  # Determine MIME type from the uploaded file
            "data": audio_bytes
        }
    ])

    try:
        parsed_response = InvoiceResponse.parse_raw(response.text)
    except ValidationError as e:
        return {"error": "Response validation failed", "details": str(e)}

    # Return the validated and formatted response as JSON
    return {"response": parsed_response.dict()}


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    image_path = f"temp_{file.filename}"
    try:
        # Check if the file is an image
        if file.content_type not in ["image/png", "image/jpeg", "image/webp", "image/heic", "image/heif"]:
            raise HTTPException(status_code=400, detail="Invalid image format")

        # Save the uploaded image
        image = Image.open(file.file)
        image.save(image_path)

        # Upload the image to Gemini API
        sample_file = genai.upload_file(path=image_path, display_name=file.filename)

        # Prompt the model with the image and predefined prompt
        response = model.generate_content([sample_file, input_prompt])

        # Parse and validate the response using Pydantic
        parsed_response = InvoiceResponse.parse_raw(response.text)

        # Return the validated and formatted response as JSON
        return {"response": parsed_response.dict()}

    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Response validation failed: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up the temporary image file
        if os.path.exists(image_path):
            os.remove(image_path)

@app.post("/text_prompt/")
async def process_invoice(invoice_text: str):
    try:
        # Send the invoice text and prompt to Gemini
        response = model.generate_content([input_prompt_text, invoice_text])

        # Parse and validate the response using Pydantic
        parsed_response = InvoiceResponse.parse_raw(response.text)

        # Return the validated and formatted response as JSON
        return {"response": parsed_response.dict()}

    except ValidationError as e:
        return {"error": "Response validation failed", "details": str(e)}

    except Exception as e:
        return {"error": "An unexpected error occurred", "details": str(e)}


'''
@app.post("/prompt/")
def read_item(item: InvoiceResponse):
    data_string = get_gemini_response_text(input_prompt_text, item.prompt)
    json_start = data_string.find('{')
    json_end = data_string.rfind('}')
    json_string = data_string[json_start:json_end+1]
    response = json.loads(json_string)

    return response
'''
'''
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
'''

#This part of code was used when I was using AssemblyAI for audio transcription, but now I have moved to gemini.
'''
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
'''

