from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Test direct model access
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1
)

# Test simple invocation
result = llm.invoke("Hello! Say hi back to me.")
print("Result:", result.content)