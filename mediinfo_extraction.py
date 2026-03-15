import os
from typing import List
from pydantic import BaseModel
from google import genai
from google.genai import types
import pytesseract
from PIL import Image

# ==========================================
# 1. DATA SCHEMAS
# ==========================================
class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str
    specialist: str 

class HealthExtraction(BaseModel):
    patient_name: str
    diagnoses: List[str]
    medications: List[Medication]
    clinical_notes: str

# ==========================================
# 2. CORE LOGIC
# ==========================================
API_KEY = ""
client = genai.Client(api_key=API_KEY)

def extract_medical_data(folder_path: str):
    combined_text_context = ""

    print(f"--- Processing folder: {folder_path} ---")

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        
        # 1. READ TEXT FILES
        if filename.lower().endswith(".txt"):
            print(f"Reading text from {filename}...")
            with open(full_path, 'r') as f:
                combined_text_context += f"\n[Document: {filename}]\n{f.read()}\n"

        # 2. LOCAL OCR FOR IMAGES (Prescriptions)
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Performing Local OCR on {filename}...")
            try:
                # This extracts the text from the image locally on your PC
                ocr_text = pytesseract.image_to_string(Image.open(full_path))
                combined_text_context += f"\n[Prescription OCR: {filename}]\n{ocr_text}\n"
            except Exception as e:
                print(f"Local OCR failed for {filename}: {e}. Make sure Tesseract is installed.")

    if not combined_text_context.strip():
        print("No readable text found in folder.")
        return None

    # 3. GENERATE CONTENT (Text Only = Lower Quota Usage)
    prompt = f"""
    Analyze the following medical text extracted from a consulting summary and a prescription.
    Extract the patient name, diagnoses, medications, and clinical notes.
    
    EXTRACTED DATA:
    {combined_text_context}
    """

    print("\nSending extracted text to Gemini (Text-only mode)...")
    
    try:
        # Changed model string to 'gemini-1.5-flash' (standard for this SDK)
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=HealthExtraction,
            ),
        )
        return response.parsed
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None

# ==========================================
# 3. RUNNER
# ==========================================
if __name__ == "__main__":
    target_folder = input("Enter folder path: ").strip()
    result = extract_medical_data(target_folder)
    
    if result:
        print("\n" + " EXTRACTION RESULTS ".center(40, "="))
        print(f"Patient: {result.patient_name}")
        print(f"Summary: {result.clinical_notes}")
        print("-" * 40)
        print("Medications:")
        for med in result.medications:
            print(f" • {med.name} | {med.dosage}")
        print("=" * 40)
