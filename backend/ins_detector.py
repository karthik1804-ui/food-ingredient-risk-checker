import re

def normalize_ocr_errors(text):
    """
    Normalizes common OCR character mistakes (like I -> 1, l -> 1, O -> 0)
    specifically where they occur in INS number contexts, so that normal words are not affected.
    """
    if not text:
        return ""
    
    # 1. Normalize when preceded by INS (case-insensitive, optional spaces, optional colons/hyphens)
    # E.g. "INS lOl" -> "INS 101", "ins OOO" -> "ins 000"
    def replace_ins_match(match):
        prefix = match.group(1)
        code = match.group(2)
        m = re.match(r'^([0-9IlO\s]+)(.*)$', code)
        if m:
            num_part = m.group(1)
            rest_part = m.group(2)
            num_part = num_part.replace('I', '1').replace('l', '1').replace('O', '0')
            return prefix + num_part + rest_part
        else:
            if len(code) >= 3:
                prefix_code = code[:4]
                rest_code = code[4:]
                prefix_code = prefix_code.replace('I', '1').replace('l', '1').replace('O', '0')
                return prefix + prefix_code + rest_code
        return match.group(0)

    # Replace INS code patterns
    text = re.sub(r'((?i:\bINS)\s*[:\-]?\s*)([0-9a-zA-Z()]+)', replace_ins_match, text)
    
    # 2. Normalize standalone numbers that contain a mix of digits and I/l/O (e.g. "1O2", "2ll")
    # Must contain at least one digit to distinguish from normal words (e.g., 'oil', 'Ill').
    def replace_candidate(match):
        num_part = match.group(1)
        suffix_part = match.group(2)
        if any(c.isdigit() for c in num_part):
            cleaned_num = num_part.replace('I', '1').replace('l', '1').replace('O', '0')
            return cleaned_num + suffix_part
        return match.group(0)
    
    text = re.sub(r'\b([0-9IlO]{3,4})([a-zA-Z]?(?:\([^)]+\))?)\b', replace_candidate, text)
    
    return text

def detect_ins(text):
    """
    Extracts all unique INS (International Numbering System) food additive codes 
    from the provided OCR text.
    
    Supports formats like:
      - INS 211
      - 211
      - INS:211
      - INS-211
      - INS211
      - Preservative (211)
      - Colour (102)
      - Acidity Regulator (330)
      - INS 101(i)
      - 150a
      - INS 160c
      - INS160c
    """
    if not text:
        return []
    
    # Normalize common OCR mistakes before extraction
    normalized_text = normalize_ocr_errors(text)
    
    # Improved pattern to support optional spaces, hyphen, colon, casing, and suffixes
    pattern = r'(?:INS\s*[:\-]?\s*|\b)(\d{3,4}[a-zA-Z]?(?:\([^)]+\))?)'
    
    matches = re.findall(pattern, normalized_text, re.IGNORECASE)
    
    # Filter out empty or purely alphabetic matches to avoid false positives
    clean_codes = []
    for code in matches:
        if any(char.isdigit() for char in code):
            clean_codes.append(code.strip())
            
    # Remove duplicates
    return list(set(clean_codes))