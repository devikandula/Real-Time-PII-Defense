
# Real-Time PII Defense  

🚀 A robust Python-based tool to automatically detect and redact **Personally Identifiable Information (PII)** from datasets.  

This project was built to identify and mask sensitive information while ensuring non-PII data is preserved correctly.  

---

## 📌 Features  
- Detects **Standalone PII**:  
  - Phone Numbers (10 digits)  
  - Aadhaar Numbers (12 digits)  
  - Passport Numbers (alphanumeric formats, e.g., P1234567)  
  - UPI IDs (e.g., user@upi, 9876543210@ybl)  

- Detects **Combinatorial PII** (only when two or more appear together):  
  - Full Name (first + last)  
  - Email Address  
  - Physical Address (street, city, pincode)  
  - Device ID / IP Address  

- Avoids **False Positives** (Non-PII):  
  - Standalone first/last names  
  - A single email without other context  
  - City/State/Pin alone  
  - Transaction IDs, Order IDs, Product details  

- Exports a **redacted dataset** with sensitive values replaced by `[REDACTED]`.  

---

## ⚡ Usage  

### 1. Clone the Repository  
```bash
git clone https://github.com/devikandula/Real-Time-PII-Defense.git
cd Real-Time-PII-Defense
````

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Detector

```bash
python detector_full_candidate_name.py input_dataset.csv
```

👉 This will generate an output file named:

```
redacted_output_Devi_Kandula.csv
```

---

## 📂 File Structure

```
Real-Time-PII-Defense/
│
├── detector_full_candidate_name.py   # Main script
├── redacted_output_Devi_Kandula.csv  # Example output file
├── requirements.txt                  # Dependencies
├── README.md                         # Documentation
└── .gitignore                        # Ignore cache, venv, etc.
```

---

## ✅ Example

**Input Dataset (iscp\_pii\_dataset.csv):**

| Name         | Email                                 | Phone Number | Aadhaar Number |
| ------------ | ------------------------------------- | ------------ | -------------- |
| Devi Kandula | [devi@mail.com](mailto:devi@mail.com) | 9876543210   | 1234 5678 9012 |

**Output (redacted\_output\_Devi\_Kandula.csv):**

| Name        | Email       | Phone Number | Aadhaar Number |
| ----------- | ----------- | ------------ | -------------- |
| \[REDACTED] | \[REDACTED] | \[REDACTED]  | \[REDACTED]    |

---

## 🛡️ Why This Project?

With increasing data regulations like **GDPR** and **DPDP Act (India)**, protecting user privacy is critical. This tool helps ensure compliance by automating the detection and redaction of sensitive information.

---

## 👩‍💻 Author

**Devi Kandula**
🔗 [GitHub Profile](https://github.com/devikandula)

---

## 📜 License

This project is licensed under the **MIT License** – free to use and modify.

