import os
import re
import json
import hashlib
import time
import requests
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────
API_KEY = os.environ.get("LLM_API_KEY", "").strip()
API_BASE = os.environ.get("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1").strip()
MODEL_ID = os.environ.get("LLM_MODEL", "qwen/qwen3.5-122b-a10b") 
CACHE_FILE = ".translation-cache.json"
SKILLS_DIR = "skills"
BATCH_SIZE = 1 # Process 1 file at a time for minimal tracking
DELAY_SECONDS = 30 # Wait seconds between files

# Regex for Chinese characters
CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def has_chinese(text):
    return bool(CHINESE_PATTERN.search(text))

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def translate_text(text):
    invoke_url = f"{API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    prompt = f"""
Translate the following Markdown content from Chinese to English. 
Maintain all Markdown formatting, code blocks, and structure perfectly.
Only translate the text content. Do not change technical terms, IDs, or file paths if they are in English.
The output must be ONLY the translated Markdown content.

Content:
{text}
"""
    
    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 16384,
        "stream": False, # Standard request is safer for preserving formatting
        "chat_template_kwargs": {"enable_thinking": True}
    }
    
    try:
        print(f"DEBUG: Sending request for translation using model {MODEL_ID} (standard)...")
        start_time = time.time()
        # Large timeout for deep-thinking models
        response = requests.post(invoke_url, headers=headers, json=payload, timeout=600)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"DEBUG: Received response in {duration:.2f} seconds.")
            
            if 'choices' in data and len(data['choices']) > 0:
                message = data['choices'][0].get('message', {})
                content = message.get('content', "")
                
                # Handle cases where content might be empty but reasoning/thinking exists
                if not content and 'reasoning_content' in message:
                    print("DEBUG: Content empty but reasoning_content found. Using reasoning_content.")
                    content = message['reasoning_content']
                
                if content:
                    print(f"DEBUG: Successfully received {len(content)} characters of translation.")
                    return content
                else:
                    print(f"DEBUG: Choice found but content is empty. Message: {json.dumps(message)}")
            else:
                print(f"DEBUG: No choices found in response. Data: {json.dumps(data)}")
        else:
            print(f"Error during translation: Status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error during translation exception: {e}")
    
    return None

def main():
    if not API_KEY:
        print("Error: LLM_API_KEY not found in environment.")
        return

    # Load cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    # Find all .md files in skills directory
    md_files = list(Path(SKILLS_DIR).rglob("*.md"))
    if os.path.exists("README.md"):
        md_files.append(Path("README.md"))

    print(f"Found {len(md_files)} Markdown files.")

    files_to_translate = []
    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not has_chinese(content):
            continue

        file_id = str(md_path)
        content_hash = get_hash(content)

        if cache.get(file_id) == content_hash:
            continue
            
        files_to_translate.append((md_path, content, content_hash))

    print(f"Queue size: {len(files_to_translate)} files need translation.")
    
    # Take only the first BATCH_SIZE files
    batch = files_to_translate[:BATCH_SIZE]
    if batch:
        print(f"Processing batch of {len(batch)} files...")
    else:
        print("No new files to translate.")
        return

    updated_count = 0
    for md_path, content, original_hash in batch:
        print(f"Translating ({updated_count+1}/{len(batch)}): {md_path} ...")
        translated = translate_text(content)
        
        if translated:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(translated)
            
            cache[str(md_path)] = original_hash
            save_cache(cache) # Save cache after EVERY file
            updated_count += 1
            print(f"  ✓ Translated and updated: {md_path}")
            
            if updated_count < len(batch):
                print(f"Waiting {DELAY_SECONDS} seconds before next file...")
                time.sleep(DELAY_SECONDS)
        else:
            print(f"  ✗ Failed to translate: {md_path}")

    print(f"Batch finished. Updated {updated_count} files.")

if __name__ == "__main__":
    main()
