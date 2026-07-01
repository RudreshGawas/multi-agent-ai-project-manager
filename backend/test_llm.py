from services.llm_service import llm_service

llm = llm_service.get_llm()

print("Calling Gemini...")

response = llm.invoke("Say hello in one sentence.")

print(response.content)