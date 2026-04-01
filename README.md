# RoyalTank_DB

`RoyalTank_DB` is a FastAPI project for storing museum tank data, predicting tank classes from images, and answering user questions about the predicted tank using OpenAI.

## Features

This project does three main things:

1. Stores tank information in a database.
2. Predicts a tank from an uploaded image using a trained model.
3. Uses OpenAI to answer a question about the predicted tank.

## Workflow

When a user uploads a tank image to the API, the system works like this:

1. The image is processed by the model in `Predict.py`.
2. The model predicts the tank name.
3. The application searches for that tank in the database.
4. The user’s question is sent to OpenAI together with the tank details.
5. The API returns:
   - the predicted tank
   - the tank record from the database
   - the chatbot response

## Project Structure

- `main.py`  
  Starts the FastAPI application and registers the routes.

- `routing.py`  
  Contains the API endpoints.

- `models.py`  
  Defines the database models and request schemas.

- `database.py`  
  Handles the database connection and session setup.

- `Predict.py`  
  Loads the trained image classification model and preprocesses uploaded images.

- `Chat.py`  
  Sends tank information and the user question to OpenAI and returns the generated response.

## Requirements

Before running the project, make sure you have:

- Python installed
- A valid database connection string
- An OpenAI API key
- The trained model file at `Classifer/tank_model.pth`

## Environment Variables

Create a `.env` file in the project root and add:

```env
DATABASE_URL=your_database_url
OPENAI_KEY=your_openai_api_key
