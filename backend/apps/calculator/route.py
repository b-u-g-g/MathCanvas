"""
from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    data = []
    for response in responses:
        data.append(response)
    print('response in route: ', response)
    return {"message": "Image processed", "data": data, "status": "success"}
"""
from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    
    responses = []
    try:
        raw_responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        for response in raw_responses:
            responses.append(response)
    except Exception as e:
        print("Error processing image or parsing API response:", e)

    # Safely print the last response if available
    if responses:
        print('response in route: ', responses[-1])
    else:
        print('No valid responses returned from analyze_image')

    return {"message": "Image processed", "data": responses, "status": "success"}
