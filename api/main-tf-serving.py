# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import tensorflow as tf
# import requests

# app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# endpoint = "http://localhost:8501/v1/models/potatoes_model:predict"

# CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

# @app.get("/ping")
# async def ping():
#     return "Hello, I am alive"

# def read_file_as_image(data) -> np.ndarray:
#     image = np.array(Image.open(BytesIO(data)))
#     return image

# @app.post("/predict")
# async def predict(
#     file: UploadFile = File(...)
# ):
#     image = read_file_as_image(await file.read())
#     img_batch = np.expand_dims(image, 0)

#     json_data = {
#         "instances": img_batch.tolist()
#     }

#     response = requests.post(endpoint, json=json_data)
#     prediction = np.array(response.json()["predictions"][0])

#     predicted_class = CLASS_NAMES[np.argmax(prediction)]
#     confidence = np.max(prediction)

#     return {
#         "class": predicted_class,
#         "confidence": float(confidence)
#     }

# if __name__ == "__main__":
#     uvicorn.run(app, host='localhost', port=8000)







# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import requests
# import os
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# app = FastAPI()

# # CORS settings
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # TensorFlow Serving endpoint
# endpoint = "http://localhost:8501/v1/models/plant_type_model:predict"

# # Updated class names for 30 plant types
# CLASS_NAMES = [
#     "Alovera", "Banana", "Bilimbi", "Cantaloupe", "Cassava", "Coconut", "Corn",
#     "Cucumber", "Curcuma", "Egg Plant", "Galangal", "Ginger", "Guava", "Kale",
#     "Long Beans", "Mango", "Orange", "Melon", "Paddy", "Papaya", "Pepper Chilli",
#     "Pineapple", "Pomelo", "Shallot", "Soybeans", "Spinach", "Sweet Potatoes",
#     "Tobacco", "WaterApple", "Watermelon"
# ]

# @app.get("/ping")
# async def ping():
#     return {"message": "Hello, I am alive!"}

# def read_file_as_image(data) -> np.ndarray:
#     """Read binary file data as a NumPy array image."""
#     try:
#         image = np.array(Image.open(BytesIO(data)).resize((128, 128)))  # Resize image
#         logging.info(f"Image shape after resizing: {image.shape}")
#         return image / 255.0  # Normalize to [0, 1]
#     except Exception as e:
#         logging.error(f"Error processing image: {e}")
#         return None

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         # Read and preprocess the uploaded file
#         temp_file_path = f"temp_{file.filename}"
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(await file.read())

#         with open(temp_file_path, "rb") as temp_file:
#             image_data = read_file_as_image(temp_file.read())

#         if image_data is None:
#             return {"error": "Invalid image data"}

#         os.remove(temp_file_path)  # Clean up temporary file

#         # Add batch dimension
#         img_batch = np.expand_dims(image_data, 0)

#         # Prepare request payload
#         json_data = {"instances": img_batch.tolist()}

#         # Send request to TensorFlow Serving
#         response = requests.post(endpoint, json=json_data)
#         response.raise_for_status()  # Raise exception if response status is not OK

#         # Parse response
#         prediction = np.array(response.json()["predictions"][0])

#         if np.any(np.isnan(prediction)):
#             logging.error(f"Prediction contains NaN values: {prediction}")
#             return {"error": "Model prediction returned invalid values (NaN)."}

#         predicted_class = CLASS_NAMES[np.argmax(prediction)]
#         confidence = np.max(prediction)

#         return {
#             "class": predicted_class,
#             "confidence": float(confidence)
#         }
#     except Exception as e:
#         logging.error(f"Error during prediction: {e}")
#         return {
#             "error": str(e)
#         }

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)





from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import requests
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TensorFlow Serving endpoint
endpoint = "http://localhost:8501/v1/models/plant_type_model:predict"

# Updated class names for 30 plant types
CLASS_NAMES = [
    "Alovera", "Banana", "Bilimbi", "Cantaloupe", "Cassava", "Coconut", "Corn",
    "Cucumber", "Curcuma", "Egg Plant", "Galangal", "Ginger", "Guava", "Kale",
    "Long Beans", "Mango", "Orange", "Melon", "Paddy", "Papaya", "Pepper Chilli",
    "Pineapple", "Pomelo", "Shallot", "Soybeans", "Spinach", "Sweet Potatoes",
    "Tobacco", "WaterApple", "Watermelon"
]

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am alive!"}

def read_file_as_image(data) -> np.ndarray:
    """Read binary file data as a NumPy array image."""
    try:
        image = np.array(Image.open(BytesIO(data)).resize((128, 128)))  # Resize image
        logging.info(f"Image shape after resizing: {image.shape}")
        return image / 255.0  # Normalize to [0, 1]
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file: {file.filename}")
        
        # Read and preprocess the uploaded file
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        logging.info(f"Saved temporary file: {temp_file_path}")

        with open(temp_file_path, "rb") as temp_file:
            image_data = read_file_as_image(temp_file.read())

        if image_data is None:
            logging.error("Failed to process image.")
            return {"error": "Invalid image data"}

        logging.info(f"Preprocessed image data: {image_data.shape}")

        os.remove(temp_file_path)  # Clean up temporary file
        logging.info(f"Temporary file removed: {temp_file_path}")

        # Add batch dimension
        img_batch = np.expand_dims(image_data, 0)
        logging.info(f"Image batch shape: {img_batch.shape}")

        # Prepare request payload
        json_data = {"instances": img_batch.tolist()}
        logging.info(f"Request payload: {json_data}")

        # Send request to TensorFlow Serving
        response = requests.post(endpoint, json=json_data)
        logging.info(f"Model server response status: {response.status_code}")
        logging.info(f"Model server response body: {response.text}")
        response.raise_for_status()  # Raise exception if response status is not OK

        # Parse response
        prediction = np.array(response.json()["predictions"][0])
        logging.info(f"Model prediction: {prediction}")

        if np.any(np.isnan(prediction)):
            logging.error(f"Prediction contains NaN values: {prediction}")
            return {"error": "Model prediction returned invalid values (NaN)."}

        predicted_class = CLASS_NAMES[np.argmax(prediction)]
        confidence = np.max(prediction)

        logging.info(f"Predicted class: {predicted_class}, Confidence: {confidence}")

        return {
            "class": predicted_class,
            "confidence": float(confidence)
        }
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
