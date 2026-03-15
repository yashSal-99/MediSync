from openai import OpenAI

# OpenRouter Configuration
# Get your key from https://openrouter.ai/keys
API_KEY = ""
BASE_URL = "https://openrouter.ai/api/v1"

# Choose your model (e.g., Gemini 2.0 Flash via OpenRouter)
MODEL_ID = "google/gemini-2.0-flash-001"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

def check_medication_risks():
    print("--- MedSync Simple Interaction Engine (OpenRouter) ---")
    
    # Take manual input from the console
    print("\n[STEP 1] Paste the Doctor's Summary & Prescription text below:")
    user_input = input("> ")

    prompt = f"""
    You are a clinical pharmacist. Analyze the following medical text for drug-drug interactions, 
    metabolic pathway conflicts (like CYP3A4), and risks based on the patient's condition.
    
    Medical Text:
    {user_input}
    
    Provide the output in this format:
    1. CONFLICTS DETECTED: (List the drugs)
    2. RISK LEVEL: (High/Medium/Low)
    3. BIOLOGICAL MECHANISM: (Explain why they conflict)
    4. RECOMMENDATION: (What should the patient do?)
    """

    print("\n🚀 Analyzing for risks...")

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "user", "content": prompt}
            ],
            # Optional: Add HTTP headers for OpenRouter rankings
            extra_headers={
                "HTTP-Referer": "http://localhost:3000", # Your site URL
                "X-Title": "MedSync Hackathon", # Your app name
            }
        )
        print("\n--- SAFETY REPORT ---")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_medication_risks()
