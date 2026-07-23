#!/usr/bin/env python3
# verify_languages.py — Quick integrity check for all language files
# Run: python verify_languages.py

import os
import re

BASE = r"C:\ТеоремаТворца"

FILES = {
    "CORE_STORY_ru.md": "ru",
    "CORE_STORY_en.md": "en",
    "CORE_STORY_es.md": "es",
    "CORE_STORY_fr.md": "fr",
    "CORE_STORY_it.md": "it",
    "CORE_STORY_ar.md": "ar",
    "CORE_STORY_zh.md": "zh",
    "CORE_STORY_hi.md": "hi",
    "CORE_STORY_ur.md": "ur",
    "CORE_STORY_pt.md": "pt",
    "CORE_STORY_bn.md": "bn",
    "00_theorem_of_creator_ru.md": "ru",
    "01_theorem_of_creator_en.md": "en",
    "02_theorem_of_creator_es.md": "es",
    "03_theorem_of_creator_fr.md": "fr",
    "04_theorem_of_creator_it.md": "it",
    "05_theorem_of_creator_ur.md": "ur",
    "06_theorem_of_creator_ar.md": "ar",
    "07_theorem_of_creator_zh.md": "zh",
    "08_theorem_of_creator_hi.md": "hi",
    "09_theorem_of_creator_pt.md": "pt",
    "10_theorem_of_creator_bn.md": "bn",
}

# Known bad patterns from previous cycles
BAD_PATTERNS = [
    r"truuQUIQUE",
    r"\\n",  # escaped newlines in markdown
    r"\\u[0-9a-fA-F]{4}",  # unicode escapes
    r"&[a-z]+;",  # HTML entities (should be actual chars)
]

# Scripts that should appear in each language
SCRIPT_CHECKS = {
    "ar": r"[\u0600-\u06FF]",
    "ur": r"[\u0600-\u06FF]",
    "hi": r"[\u0900-\u097F]",
    "bn": r"[\u0980-\u09FF]",
    "zh": r"[\u4e00-\u9fff]",
}

# Minimum file sizes (bytes) - CJK languages use ~3 bytes/char so lower threshold
MIN_SIZES = {
    "zh": 3000,
    "ja": 3000,
    "ko": 3000,
    "default": 5000,
}

def check_file(path, lang):
    issues = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError as e:
        return [f"ENCODING ERROR: {e}"]

    # Check for bad patterns
    for pattern in BAD_PATTERNS:
        matches = list(re.finditer(pattern, content))
        if matches:
            issues.append(f"BAD PATTERN '{pattern}': {len(matches)} occurrences")

    # Check script presence
    if lang in SCRIPT_CHECKS:
        if not re.search(SCRIPT_CHECKS[lang], content):
            issues.append(f"MISSING {lang.upper()} SCRIPT CHARACTERS")

    # Check Cannabis Action 8.5 presence
    cannabis_markers = ["Cannabis", "cannabis", "Каннабис", "कैनाबिस", "大麻", "القنب", "Cannabis sativa", "ক্যানাবিস", " القنّب", "القنب الهندي"]
    if not any(m in content for m in cannabis_markers):
        issues.append("MISSING CANNABIS ACTION 8.5 REFERENCE")

    # Check file size (too small = probably broken) - adjusted for CJK
    min_size = MIN_SIZES.get(lang, MIN_SIZES["default"])
    if len(content) < min_size:
        issues.append(f"FILE TOO SMALL ({len(content)} chars, min {min_size})")

    return issues

def main():
    print("=" * 60)
    print("LANGUAGE FILE INTEGRITY CHECK")
    print("=" * 60)
    
    all_ok = True
    for fname, lang in FILES.items():
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            print(f"❌ MISSING: {fname}")
            all_ok = False
            continue
        
        issues = check_file(path, lang)
        if issues:
            print(f"⚠️  {fname} ({lang})")
            for issue in issues:
                print(f"   - {issue}")
            all_ok = False
        else:
            size = os.path.getsize(path)
            print(f"✅ {fname} ({lang}) — {size:,} bytes")
    
    print("=" * 60)
    if all_ok:
        print("ALL CHECKS PASSED")
    else:
        print("ISSUES FOUND — SEE ABOVE")
    print("=" * 60)

if __name__ == "__main__":
    main()