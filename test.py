import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBARK48U8sJWSL8GajxiBpPO8TjqoY3B6g"

# Load Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Ask AI
response = llm.invoke("Say hello")

# Print Response
print(response.content)