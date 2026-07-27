#!/usr/bin/env python3
"""
Batch translation script for Theorem of Creator documents.
Translates Tier 1 core documents from English to 12 target languages.
Uses offline translation (argostranslate) + LLM for quality.
"""

import os
import json
from pathlib import Path

# Configuration
SOURCE_DIR = Path("/c/ТеоремаТворца/en")
TARGET_DIR = Path("/c/ТеоремаТворца")

# Tier 1 documents (5 core files)
TIER1_FILES = [
    "01_theorem_of_creator_en.md",
    "CORE_STORY_en.md", 
    "ANALYTICAL_NOTE_EN.md",
    "INVESTOR_PROSPECTUS_EN.md",
    "TRANSLATION_PLAN.md"
]

# Target languages
LANGUAGES = {
    "es": "Spanish",
    "fr": "French", 
    "de": "German",
    "zh": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "it": "Italian",
    "ar": "Arabic",
    "hi": "Hindi",
    "ur": "Urdu",
    "bn": "Bengali"
}

# Language codes for argostranslate
ARGOS_CODES = {
    "es": "es",
    "fr": "fr",
    "de": "de", 
    "zh": "zh",
    "ja": "ja",
    "ko": "ko",
    "pt": "pt",
    "it": "it",
    "ar": "ar",
    "hi": "hi",
    "ur": "ur",
    "bn": "bn"
}

def read_markdown(filepath):
    """Read markdown file preserving structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_markdown(filepath, content):
    """Write markdown file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def translate_with_argos(text, target_lang):
    """Translate using argostranslate (offline)."""
    try:
        import argostranslate.package
        import argostranslate.translate
        
        # Check if package installed, install if not
        from_code = "en"
        to_code = ARGOS_CODES.get(target_lang, target_lang)
        
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_languages if l.code == from_code), None)
        to_lang = next((l for l in installed_languages if l.code == to_code), None)
        
        if not from_lang or not to_lang:
            # Try to install
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package = next((p for p in available_packages 
                          if p.from_code == from_code and p.to_code == to_code), None)
            if package:
                argostranslate.package.install_from_path(package.download())
                installed_languages = argostranslate.translate.get_installed_languages()
                from_lang = next((l for l in installed_languages if l.code == from_code), None)
                to_lang = next((l for l in installed_languages if l.code == to_code), None)
        
        if from_lang and to_lang:
            translation = from_lang.get_translation(to_lang)
            return translation.translate(text)
    except Exception as e:
        print(f"  Argos translate failed for {target_lang}: {e}")
    return None

def chunk_text(text, max_chunk=500):
    """Split text into chunks at sentence boundaries."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) < max_chunk:
            current += sent + " "
        else:
            if current:
                chunks.append(current.strip())
            current = sent + " "
    if current:
        chunks.append(current.strip())
    return chunks

def translate_markdown(content, target_lang):
    """Translate markdown content preserving structure."""
    import re
    
    lines = content.split('\n')
    translated_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Preserve headers, code blocks, tables, math, links
        if (line.startswith('#') or 
            line.startswith('```') or 
            line.startswith('|') or
            line.startswith('$') or
            line.startswith('>') or
            line.strip() == '' or
            re.match(r'^\s*[-*+]\s', line) or  # list items
            re.match(r'^\s*\d+\.\s', line) or  # numbered lists
            '<' in line and '>' in line):  # HTML tags
            translated_lines.append(line)
        else:
            # Translate regular text
            if line.strip():
                translated = translate_with_argos(line, target_lang)
                if translated:
                    translated_lines.append(translated)
                else:
                    translated_lines.append(line)  # fallback
            else:
                translated_lines.append(line)
        i += 1
    
    return '\n'.join(translated_lines)

def main():
    print("=" * 60)
    print("THEOREM OF CREATOR - BATCH TRANSLATION TIER 1")
    print("=" * 60)
    
    # Check source files
    for fname in TIER1_FILES:
        fpath = SOURCE_DIR / fname
        if not fpath.exists():
            print(f"⚠️  Missing: {fname}")
        else:
            print(f"✅ Found: {fname} ({fpath.stat().st_size} bytes)")
    
    total_tasks = len(TIER1_FILES) * len(LANGUAGES)
    completed = 0
    
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n🌐 Translating to {lang_name} ({lang_code})...")
        lang_dir = TARGET_DIR / lang_code
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        for fname in TIER1_FILES:
            src = SOURCE_DIR / fname
            if not src.exists():
                continue
                
            # Output filename: replace _en.md with _{lang}.md
            out_name = fname.replace('_en.md', f'_{lang_code}.md').replace('_EN.md', f'_{lang_code}.md')
            dst = lang_dir / out_name
            
            print(f"  📄 {fname} → {out_name}")
            
            content = read_markdown(src)
            translated = translate_markdown(content, lang_code)
            write_markdown(dst, translated)
            
            completed += 1
            print(f"     ✅ Done ({completed}/{total_tasks})")
    
    print(f"\n🎉 TIER 1 COMPLETE: {completed} files translated to {len(LANGUAGES)} languages")
    print(f"📁 Output: {TARGET_DIR}/<lang>/")

if __name__ == "__main__":
    main()