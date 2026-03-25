from openai import OpenAI
from models import Mesuem_Tanks
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def chat_with_gpt(User_Question: str, tank_info: Mesuem_Tanks | None):

    prompt = f"""Tank info:
Name: {tank_info.Name if tank_info else "Unknown"}
Description: {tank_info.Description if tank_info else "Unknown"}
Country: {tank_info.Country if tank_info else "Unknown"}
Year: {tank_info.Year if tank_info else "Unknown"}

Question: {User_Question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content