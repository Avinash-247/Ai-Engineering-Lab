from dotenv import load_dotenv
import os
load_dotenv()
print("GOOGLE_GENAI_USE_VERTEXAI =", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("GOOGLE_CLOUD_PROJECT =", os.getenv("GOOGLE_CLOUD_PROJECT"))
print("GOOGLE_CLOUD_LOCATION =", os.getenv("GOOGLE_CLOUD_LOCATION"))