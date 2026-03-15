import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai

# 1. Define the Output Schema for the Engine
class DrugConflict(BaseModel):
    interacting_drugs: List[str] = Field(description="The names of the drugs that conflict")
    risk_level: str = Field(description="High, Medium, or Low")
    mechanism: str = Field(description="The biological or chemical reason for the conflict (e.g., Enzyme CYP3A4 inhibition)")
    severity_description: str = Field(description="What happens to the patient? (e.g., Increased bleeding risk)")
    recommendation: str = Field(description="Actionable advice for the doctor or patient")

class InteractionReport(BaseModel):
    conflicts: List[DrugConflict]
    holistic_summary: str = Field(description="A summary of how these medications interact as a complete system")

# 2. Initialize the Gemini Client
# Replace with your actual API Key
client = genai.Client(api_key="")

def run_interaction_engine(extracted_data_json: str):
    """
    This function takes the JSON string from your previous extraction step
    and analyzes it for complex drug-drug and drug-condition interactions.
    """
    
    system_instruction = """
    You are a Senior Clinical Pharmacologist AI. 
    Your goal is to identify complex medication interactions that simple pairwise checks miss.
    
    Analyze the provided patient data for:
    1. Direct Drug-Drug Interactions (e.g., Warfarin + Ibuprofen).
    2. Metabolic Pathway Conflicts: Identify if multiple drugs compete for the same liver enzymes (e.g., CYP450, CYP3A4).
    3. Drug-Condition Conflicts: Check if a drug is dangerous given the patient's lab results (e.g., NSAIDs if Creatinine is High).
    4. Cascading Effects: Where one drug alters the metabolism of another, leading to toxicity.
    """

    prompt = f"Analyze this patient health data and provide a detailed interaction report: {extracted_data_json}"
    response = client.models.generate_content(
        # Use EXACTLY this string:
        model='gemini-2.0-flash', 
        contents=prompt,
        config={
            'system_instruction': system_instruction,
            'response_mime_type': 'application/json',
            'response_schema': InteractionReport,
        },
    )
    
    return response.parsed

# 3. Demo Execution
if __name__ == "__main__":
    # This represents the JSON output from your first extraction script
    dummy_extracted_data = """
    {
        "patient_name": "Rajesh Kumar",
        "diagnoses": ["Hypertension", "Type 2 Diabetes", "Chronic Kidney Disease"],
        "medications": [
            {"name": "Atorvastatin", "dosage": "40mg", "frequency": "Daily", "specialist": "Cardiologist"},
            {"name": "Warfarin", "dosage": "5mg", "frequency": "Daily", "specialist": "Cardiologist"},
            {"name": "Ibuprofen", "dosage": "400mg", "frequency": "As needed", "specialist": "Neurologist"},
            {"name": "Clarithromycin", "dosage": "500mg", "frequency": "Twice daily", "specialist": "General Physician"}
        ],
        "biomarkers": [
            {"name": "Creatinine", "value": 1.8, "unit": "mg/dL", "status": "HIGH"}
        ]
    }
    """
    
    print("🚀 Running MedSync Drug Interaction Engine...")
    report = run_interaction_engine(dummy_extracted_data)
    
    print(f"\nReport for: {dummy_extracted_data.split('patient_name\": \"')[1].split('\"')[0]}")
    print("-" * 30)
    
    for conflict in report.conflicts:
        print(f"⚠️ [{conflict.risk_level}] {', '.join(conflict.interacting_drugs)}")
        print(f"Mechanism: {conflict.mechanism}")
        print(f"Risk: {conflict.severity_description}")
        print(f"Action: {conflict.recommendation}\n")
    
    print(f"📝 Holistic Summary: {report.holistic_summary}")
