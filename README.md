diff --git a/c:\Users\hussa\Desktop\RoyalTank_DB\README.md b/c:\Users\hussa\Desktop\RoyalTank_DB\README.md
--- a/c:\Users\hussa\Desktop\RoyalTank_DB\README.md
+++ b/c:\Users\hussa\Desktop\RoyalTank_DB\README.md
@@ -0,0 +1,133 @@
+# RoyalTank_DB
+
+`RoyalTank_DB` is a small FastAPI project for working with museum tank data.
+
+It does three main things:
+
+1. Stores tank information in a database.
+2. Predicts a tank from an uploaded image using a trained model.
+3. Uses OpenAI to answer a question about the predicted tank.
+
+## How the project works
+
+When you upload a tank image to the API:
+
+1. The image is processed by the model in `Predict.py`.
+2. The model predicts the tank name.
+3. The app looks up that tank in the database.
+4. Your question is sent to OpenAI together with the tank details.
+5. The API returns the prediction, the tank record, and a chatbot response.
+
+## Project files
+
+- `main.py` starts the FastAPI app and loads the routes.
+- `routing.py` contains the API endpoints.
+- `models.py` defines the database table and request schema.
+- `database.py` connects the app to the database.
+- `Predict.py` loads the image classification model and preprocesses images.
+- `Chat.py` sends tank information and the user question to OpenAI.
+
+## Requirements
+
+Make sure you have:
+
+- Python installed
+- A working database connection string
+- An OpenAI API key
+- The trained model file at `Classifer/tank_model.pth`
+
+## Environment variables
+
+Create a `.env` file with:
+
+```env
+DATABASE_URL=your_database_url
+OPENAI_KEY=your_openai_api_key
+```
+
+## Install dependencies
+
+If your virtual environment is not active yet, activate it first, then install the needed packages:
+
+```bash
+pip install fastapi uvicorn sqlalchemy python-dotenv openai torch torchvision pillow python-multipart
+```
+
+## Run the API
+
+Start the FastAPI server with:
+
+```bash
+uvicorn main:app --reload
+```
+
+The API will usually be available at:
+
+```text
+http://127.0.0.1:8000
+```
+
+Interactive docs:
+
+```text
+http://127.0.0.1:8000/docs
+```
+
+## API endpoints
+
+### 1. Add a tank
+
+`POST /tanks/`
+
+Use this endpoint to save tank information in the database.
+
+Example body:
+
+```json
+{
+  "Name": "Tiger I",
+  "Description": "German heavy tank",
+  "Country": "Germany",
+  "Year": 1942
+}
+```
+
+### 2. Get tank info from an image
+
+`POST /tanks/info/{Question}`
+
+Use this endpoint to:
+
+- upload a tank image
+- predict which tank it is
+- ask a question about that tank
+
+You must send the image as a file upload.
+
+Example idea:
+
+- Question in the URL: `When was this tank used?`
+- File: the tank image
+
+### 3. List all tanks
+
+`GET /tanks/list/`
+
+Returns every tank stored in the database.
+
+## Notes
+
+- The model file must exist or prediction will fail.
+- `Predict.py` also depends on the training folder path used to recover class names.
+- The OpenAI request in `Chat.py` uses the `gpt-4o-mini` model.
+
+## Summary
+
+This project combines:
+
+- FastAPI for the backend
+- SQLAlchemy for the database
+- PyTorch for image classification
+- OpenAI for question answering
+
+It is useful if you want to build a simple tank recognition and information system.
