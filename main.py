import pypdf
import json
import os
import sys

# Add the current directory to sys.path to allow importing from 'src'
sys.path.append(os.getcwd())

from src.parser.cleaner import CleanText
from src.parser.segmenter import segment_symptoms
from src.parser.mapper import map_segment


def run_pipeline(input_path: str, output_path: str):
    print(f"🚀 Starting Bio-Mapping Engine Pipeline...")
    print(f"📂 Input: {input_path}")

    if not os.path.exists(input_path):
        print(f"❌ Error: Input file not found at {input_path}")
        return

    # 1. Extraction
    print("📖 Reading PDF and extracting text...")
    try:
        reader = pypdf.PdfReader(input_path)
        full_text = ""
        total_pages = len(reader.pages)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
            if (i + 1) % 50 == 0:
                print(f"   ... processed {i+1}/{total_pages} pages")
    except Exception as e:
        print(f"❌ Error during PDF extraction: {e}")
        return

    # 2. Cleaning
    print("🧹 Cleaning text...")
    cleaner = CleanText()
    cleaned_text = cleaner.clean(full_text)

    # 3. Segmentation
    print("✂️ Segmenting text into symptom blocks...")
    segments = segment_symptoms(cleaned_text)
    print(f"   Found {len(segments)} potential symptom blocks.")

    # 4. Mapping
    print("🧠 Mapping segments to structured data (this may take a moment)...")
    processed_data = []
    for idx, segment in enumerate(segments):
        try:
            mapped = map_segment(segment)
            if mapped is not None and "error" not in mapped:
                processed_data.append(mapped)
            if (idx + 1) % 50 == 0:
                print(f"   ... mapped {idx+1}/{len(segments)} segments")
        except Exception as e:
            print(f"⚠️ Warning: Failed to map segment {idx}: {e}")

    # 5. Save Output
    print(f"💾 Saving {len(processed_data)} records to {output_path}...")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        print("✅ Pipeline completed successfully!")
    except Exception as e:
        print(f"❌ Error saving output: {e}")


if __name__ == "__main__":
    INPUT_FILE = "data/raw/Biodescodificacion.pdf"
    OUTPUT_FILE = "data/processed/processed_data.json"

    run_pipeline(INPUT_FILE, OUTPUT_FILE)
