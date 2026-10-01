from collections import Counter

def calculate_risk(additives):
    """
    Calculates overall risk score, level, and generates a descriptive reason based on detected additives.
    
    Returns:
        tuple: (overall_score, overall_level, overall_risk_reason)
    """
    if not additives:
        return 0, "Low", "• No additives detected\n• The product is estimated to be safe"

    # Step 1: Collect all detected additive risk scores and sort descending
    scores = sorted([float(item.get("risk_score", 0)) for item in additives], reverse=True)
    
    primary = scores[0]
    secondary_contribution = 0.0
    
    # Calculate secondary contribution with decaying weight: 0.5^i for S_(i+1)
    for idx, score in enumerate(scores[1:]):
        weight = 0.5 ** (idx + 1)
        secondary_contribution += score * weight
        
    raw_score = primary + secondary_contribution
    
    # Additive Count Bonus
    count = len(additives)
    bonus = 0
    if count > 8:
        bonus = 20
    elif count > 5:
        bonus = 15
    elif count > 3:
        bonus = 8
        
    score_with_bonus = raw_score + bonus
    
    # High Risk Rule
    has_high_risk = any(item.get("high_risk_flag") in (1, True, "1", "TRUE") for item in additives)
    if has_high_risk:
        score_with_bonus = max(score_with_bonus, 65)
        
    # Clamp and Round
    overall_score = min(round(score_with_bonus), 100)
    
    # Determine Risk Level
    if overall_score <= 30:
        level = "Low"
    elif overall_score <= 60:
        level = "Moderate"
    else:
        level = "High"
        
    # Generate Overall Risk Reason Bullet Points
    reasons = []
    
    # 1. Total Additive Count
    reasons.append(f"Contains {count} additive{'s' if count != 1 else ''}")
    
    # 2. High-Risk Additive Count
    high_risk_count = sum(1 for item in additives if item.get("high_risk_flag") in (1, True, "1", "TRUE"))
    if high_risk_count > 0:
        reasons.append(f"Contains {high_risk_count} high-risk additive{'s' if high_risk_count != 1 else ''}")
        
    # 3. Highest risk score
    reasons.append(f"Highest additive risk score is {round(primary)}")
    
    # 4. Check category counts (e.g. preservatives)
    categories = [item.get("category", "").strip() for item in additives if item.get("category")]
    category_counts = Counter(categories)
    for cat, cat_count in category_counts.items():
        if cat_count > 1:
            # Pluralize category name (e.g., Preservative -> preservatives)
            cat_plural = cat.lower() + "s" if not cat.lower().endswith("s") else cat.lower()
            reasons.append(f"Multiple {cat_plural} detected")
            
    overall_reason = "\n".join(f"• {r}" for r in reasons)
    
    return overall_score, level, overall_reason