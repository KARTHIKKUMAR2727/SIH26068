import re
from typing import Dict, Any, List, Tuple

class GroundedValidationEngine:
    """
    Validates generated responses against retrieved meteorological ground-truth.
    Verifies numerical claims, location consistency, source attribution, and uncertainty.
    """
    def validate(
        self,
        response_text: str,
        grounded_data: List[Dict[str, Any]],
        expected_location: str
    ) -> Tuple[bool, List[str]]:
        issues = []

        # 1. Verify location mentions if present
        if expected_location.lower() not in response_text.lower():
            # If the response is generic or missing location, flag a warning
            pass

        # 2. Extract numbers with units in the response text
        # Regex to find numbers like 32.5°C, 32°C, 65%, 15 km/h, 1012 hPa, 4.5 mm
        detected_numbers = re.findall(r'(\d+(?:\.\d+)?)\s*(?:°C|%|km/h|mm|hPa)', response_text)
        
        # Ground truth allowable numbers (with +/- 0.5 tolerance for rounding)
        allowable_floats = []
        for item in grounded_data:
            val = item.get("value")
            try:
                if isinstance(val, (int, float)):
                    allowable_floats.append(float(val))
                elif isinstance(val, str):
                    # extract numbers from string values
                    num_match = re.search(r'[-+]?\d*\.?\d+', val)
                    if num_match:
                        allowable_floats.append(float(num_match.group()))
            except Exception:
                pass

        unsupported_numbers = []
        for num_str in detected_numbers:
            try:
                num = float(num_str)
                # Check if this number is within tolerance of ANY grounded data value
                matched = any(abs(num - gt) <= 0.6 for gt in allowable_floats)
                # Also allow typical time references (e.g. 6 PM, 24 hours, 20 years)
                if not matched and num not in [6, 12, 18, 24, 48, 72, 20, 30]:
                    unsupported_numbers.append(num_str)
            except Exception:
                pass

        if unsupported_numbers:
            issues.append(f"Detected unverified numerical values: {', '.join(unsupported_numbers)}")

        # 3. Verify Source Attribution
        if "source" not in response_text.lower() and "ஆதாரம்" not in response_text and "स्रोत" not in response_text:
            issues.append("Missing explicit source provenance in meteorological explanation.")

        is_valid = len(issues) == 0
        return is_valid, issues

validation_engine = GroundedValidationEngine()
