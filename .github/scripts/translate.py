import os
import re
import json
import hashlib
import time
from pathlib import Path
from google import genai
from google.genai import types

# ── Configuration ─────────────────────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY")
CACHE_FILE = ".translation-cache.json"
MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]
SKILLS_DIR = "skills"

# Regex for Chinese characters
CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def has_chinese(text):
    return bool(CHINESE_PATTERN.search(text))

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def translate_text(client, text):
    prompt = f"""
Translate the following Markdown content from Chinese to English. 
Maintain all Markdown formatting, code blocks, and structure perfectly.
Only translate the text content. Do not change technical terms, IDs, or file paths if they are in English.
The output must be ONLY the translated Markdown content.

Content:
{text}
"""
    
    for model_id in MODELS:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                )
            )
            if response.text:
                return response.text
        except Exception as e:
            print(f"Error with {model_id}: {e}")
            continue
    
    return None

def main():
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=API_KEY)
    
    # Load cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    # Find all .md files in skills directory
    md_files = list(Path(SKILLS_DIR).rglob("*.md"))
    # Also include the root README.md
    if os.path.exists("README.md"):
        md_files.append(Path("README.md"))

    print(f"Found {len(md_files)} Markdown files.")

    updated_count = 0
    
    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not has_chinese(content):
            continue

        file_id = str(md_path)
        content_hash = get_hash(content)

        if cache.get(file_id) == content_hash:
            # Check if an English version already exists (overlay strategy)
            # Actually, in this script we overwrite the file because it's a dedicated sync-translate repo
            continue

        print(f"Translating: {md_path} ...")
        translated = translate_text(client, content)
        
        if translated:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(translated)
            
            cache[file_id] = get_hash(content) # Cache the ORIGINAL hash
            updated_count += 1
            print(f"  ✓ Translated and updated.")
            # Rate limiting sleep
            time.sleep(1)
        else:
            print(f"  ✗ Failed to translate.")

    # Save cache
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"Finished. Updated {updated_count} files.")

if __name__ == "__main__":
    main()
