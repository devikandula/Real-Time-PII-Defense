import pandas as pd
import json
import re
import sys

# =====================
# Masking Functions
# =====================
def mask_phone(phone: str) -> str:
    phone = str(phone).strip()
    if len(phone) == 10 and phone.isdigit():
        return phone[:2] + "XXXXXX" + phone[-2:]
    return "[INVALID_PHONE]"

def mask_aadhar(aadhar: str) -> str:
    aadhar = str(aadhar).strip()
    if re.fullmatch(r"\d{12}", aadhar):
        return "XXXX XXXX " + aadhar[-4:]
    return "[INVALID_AADHAR]"

def mask_passport(passport: str) -> str:
    passport = str(passport).strip()
    if re.fullmatch(r"[A-Z][0-9]{7}", passport):
        return passport[0] + "XXXXXXX"
    return "[INVALID_PASSPORT]"

def mask_upi(upi: str) -> str:
    upi = str(upi).strip()
    if "@" in upi:
        user, domain = upi.split("@", 1)
        if user:
            return user[:2] + "XXX" + user[2:] + "@" + domain
    return "[INVALID_UPI]"

def mask_name(name: str) -> str:
    parts = str(name).split()
    return " ".join([p[0] + "X" * (len(p) - 1) for p in parts if p])

def mask_address(address: str) -> str:
    return "[REDACTED_ADDRESS]" if address else address

def mask_ip(ip: str) -> str:
    return "[REDACTED_IP]" if ip else ip

def mask_device(device: str) -> str:
    return "[REDACTED_DEVICE]" if device else device

# =====================
# PII Detection
# =====================
def detect_standalone_pii(record: dict) -> bool:
    pii_detected = False
    try:
        if "phone" in record and re.fullmatch(r"\d{10}", str(record["phone"])):
            record["phone"] = mask_phone(record["phone"])
            pii_detected = True
        if "aadhar" in record and re.fullmatch(r"\d{12}", str(record["aadhar"])):
            record["aadhar"] = mask_aadhar(record["aadhar"])
            pii_detected = True
        if "passport" in record and re.fullmatch(r"[A-Z]\d{7}", str(record["passport"])):
            record["passport"] = mask_passport(record["passport"])
            pii_detected = True
        if "upi_id" in record and re.fullmatch(r"[\w\d]+@[\w\d]+", str(record["upi_id"])):
            record["upi_id"] = mask_upi(record["upi_id"])
            pii_detected = True
    except Exception:
        pass
    return pii_detected

def detect_combinatorial_pii(record: dict) -> bool:
    combinatorial_fields = ["name", "email", "address", "ip_address", "device_id"]
    present = [f for f in combinatorial_fields if f in record and record[f]]
    if len(present) >= 2:
        for f in present:
            try:
                if f == "name":
                    record[f] = mask_name(record[f])
                elif f == "email":
                    record[f] = "[REDACTED_EMAIL]"
                elif f == "address":
                    record[f] = mask_address(record[f])
                elif f == "ip_address":
                    record[f] = mask_ip(record[f])
                elif f == "device_id":
                    record[f] = mask_device(record[f])
            except Exception:
                record[f] = "[REDACTION_ERROR]"
        return True
    return False

# =====================
# Main Processing
# =====================
def process_csv(input_file: str, output_file: str):
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"❌ Error reading input file: {e}")
        sys.exit(1)

    redacted_rows = []
    for _, row in df.iterrows():
        try:
            data = json.loads(row.get("data_json", "{}"))
        except Exception:
            data = {}

        is_pii = False
        if detect_standalone_pii(data):
            is_pii = True
        if detect_combinatorial_pii(data):
            is_pii = True

        redacted_rows.append({
            "record_id": row.get("record_id", "UNKNOWN"),
            "redacted_data_json": json.dumps(data),
            "is_pii": is_pii
        })

    redacted_df = pd.DataFrame(redacted_rows)
    try:
        redacted_df.to_csv(output_file, index=False)
        print(f"✅ Redacted CSV saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving output file: {e}")

# =====================
# CLI Entry Point
# =====================
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 detector_Devi_Kandula.py iscp_pii_dataset.csv")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = "redacted_output_Devi_Kandula.csv"
    process_csv(input_csv, output_csv)
