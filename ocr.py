import os
import easyocr

# 1. Initialize the reader (downloads models on the first run)
# 'gpu=False' if you don't have an NVIDIA GPU; set to True if you do!
reader = easyocr.Reader(['en'], gpu=False) 

def process_medical_folder(folder_path):
    # Supported formats
    image_extensions = ('.png', '.jpg', '.jpeg')
    text_extensions = ('.txt')

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    print(f"--- Scanning Folder: {folder_path} ---\n")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # --- CASE 1: PRESCRIPTION (IMAGE) ---
        if filename.lower().endswith(image_extensions):
            print(f"📸 [IMAGE FOUND]: {filename} - Extracting with EasyOCR...")
            try:
                results = reader.readtext(file_path, detail=0)
                print("Extracted Content:")
                print(" | ".join(results) if results else "[No text found]")
                print("-" * 50)
            except Exception as e:
                print(f"Error reading image {filename}: {e}")

        # --- CASE 2: SUMMARY (TEXT) ---
        elif filename.lower().endswith(text_extensions):
            print(f"📄 [TEXT FOUND]: {filename} - Reading content...")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("Extracted Content:")
                    print(content.strip())
                    print("-" * 50)
            except Exception as e:
                print(f"Error reading text file {filename}: {e}")

if __name__ == "__main__":
    # Point this to your folder
    target_folder = r"C:\yash\MediSync\yash" 
    process_medical_folder(target_folder)