
# from fastapi import FastAPI, File, UploadFile

# from fastapi.middleware.cors import CORSMiddleware

# from fastapi.responses import JSONResponse
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import uvicorn
# import os

# # Initialize FastAPI app
# app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:5137",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # React app origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# # Constants
# MODEL_PATH = "../training/plant_recognition_model_v2_2.keras"
# IMAGE_SIZE = 128
# CLASS_NAMES = [
#     "Alovera", "Banana", "Bilimbi", "Cantaloupe", "Cassava", "Coconut", "Corn", "Cucumber", "Curcuma", "Egg Plant", "Galangal", "Ginger", "Guava", "Kale", "Long Beans", "Mango", "Orange", "Melon", "Paddy", "Papaya", "Pepper Chilli", "Pineapple", "Pomelo", "Shallot", "Soybeans", "Spinach", "Sweet Potatoes", "Tobacco", "WaterApple", "Watermelon"
# ]

# # Load model
# if os.path.exists(MODEL_PATH):
#     print("Loading model...")
#     model = load_model(MODEL_PATH)
# else:
#     raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Plant Type Detection API!"}

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         # Save uploaded file temporarily
#         temp_file_path = f"temp_{file.filename}"
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(await file.read())

#         # Preprocess the saved image file
#         img = image.load_img(temp_file_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
#         img_array = image.img_to_array(img) / 255.0
#         img_array = np.expand_dims(img_array, axis=0)

#         # Perform prediction
#         predictions = model.predict(img_array)
#         predicted_class_idx = np.argmax(predictions[0])
#         predicted_class = CLASS_NAMES[predicted_class_idx]
#         confidence = float(predictions[0][predicted_class_idx])

#         # Clean up temporary file
#         os.remove(temp_file_path)

#         # Return response
#         return {
#             "class": predicted_class,
#             "confidence": confidence
#         }
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": str(e)}
#         )


# # Run the app
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)




from fastapi import FastAPI, File, UploadFile

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5137",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Constants
MODEL_PATH = "../training/plant_recognition_model_v2_3.keras"
IMAGE_SIZE = 128
CLASS_NAMES = [
    "Alstonia Scholaris diseased", "Alstonia Scholaris healthy", "Arjun diseased", "Arjun healthy", "Bael diseased", "Basil healthy", "Chinar diseased", "Chinar healthy", "Gauva diseased", "Gauva healthy", "Jamun diseased", "Jamun healthy", "Jatropha diseased", "Jatropha healthy", "Lemon diseased", "Lemon healthy", "Mango diseased", "Mango healthy", "Pomegranate diseased", "Pomegranate healthy", "Pongamia Pinnata diseased", "Pongamia Pinnata healthy"
]

# Load model
if os.path.exists(MODEL_PATH):
    print("Loading model...")
    model = load_model(MODEL_PATH)
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Type Detection API!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Preprocess the saved image file
        img = image.load_img(temp_file_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Perform prediction
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx])

        # Clean up temporary file
        os.remove(temp_file_path)

        # Return response
        return {
            "class": predicted_class,
            "confidence": confidence
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)