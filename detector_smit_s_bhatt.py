import re
import json
import pandas as pd

# ====== CONFIG ======
file_path = "F:\\PythonProject\\FlipkartCTF\\iscp_pii_dataset_-_Sheet1.csv"
output_file = "redacted_output_max_score.csv"

# Regex patterns
standalone_pii_patterns = {
    "Phone": r"\b(?:\+91|0)?\d{10}\b",
    "Aadhar": r"\b\d{12}\b",
    "Passport": r"\b[A-Z]\d{7}\b",
    "UPI": r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z]{2,}\b",
    "IP": r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
}

combinatorial_pii_fields = ["name", "email", "address", "device_id", "ip_address"]

# Partial redaction functions
def redact_name(name):
    if not isinstance(name, str):
        return name
    parts = name.split()
    redacted_parts = []
    for p in parts:
        if len(p) > 1:
            redacted_parts.append(p[0] + "X" * (len(p)-1))
        else:
            redacted_parts.append(p)
    return " ".join(redacted_parts)

def redact_email(email):
    if not isinstance(email, str):
        return email
    parts = email.split("@")
    if len(parts) == 2:
        user, domain = parts
        if len(user) > 2:
            user = user[:2] + "X" * (len(user)-2)
        return user + "@" + domain
    return email

def detect_and_redact_pii(data_dict):
    is_pii = False
    combinatorial_count = 0
    redacted = {}

    for key, value in data_dict.items():
        # Standalone PII
        val_str = str(value)
        redacted_val = val_str
        for pii_name, pattern in standalone_pii_patterns.items():
            if re.search(pattern, val_str):
                redacted_val = "[REDACTED]"
                is_pii = True

        # Combinatorial PII partial redaction
        if key.lower() in combinatorial_pii_fields:
            combinatorial_count += 1
            if key.lower() == "name":
                redacted_val = redact_name(val_str)
            elif key.lower() == "email":
                redacted_val = redact_email(val_str)
            else:
                redacted_val = "[REDACTED]"

        redacted[key] = redacted_val

    # If 2+ combinatorial PII exist, count as PII
    if combinatorial_count >= 2:
        is_pii = True

    return redacted, is_pii

# Load CSV
df = pd.read_csv(file_path)

# Process each JSON record
output_records = []
for index, row in df.iterrows():
    try:
        data_json = json.loads(row["Data_json"])
    except Exception:
        data_json = {}
    redacted_json, is_pii_flag = detect_and_redact_pii(data_json)
    output_records.append({
        "record_id": row["record_id"],
        "redacted_data_json": json.dumps(redacted_json),
        "is_pii": is_pii_flag
    })

# Save CSV
output_df = pd.DataFrame(output_records)
output_df.to_csv(output_file, index=False)
print(f"[+] Redacted file saved as {output_file}")

# Optional: search for ISCP flag
flag_found = False
for val in output_df["redacted_data_json"]:
    if "ISCP" in val:
        print(f"[FLAG FOUND] {val}")
        flag_found = True

if not flag_found:
    print("[!] No flag found in this file.")
