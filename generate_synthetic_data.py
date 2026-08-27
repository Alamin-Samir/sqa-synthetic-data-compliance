import hashlib
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()
Faker.seed(42)  # For consistent output


# 1. Email Masking (GDPR Pseudonymization)
def mask_email(email):
    parts = email.split("@")
    user = parts[0]
    domain = parts
    if len(user) <= 2:
        masked_user = user[0] + "***"
    else:
        masked_user = user[0] + "***" + user[-1]
    return f"{masked_user}@{domain}"


# 2. Credit Card Masking (PCI-DSS Standard: Keep only last 4 digits)
def mask_card(card_number):
    clean_card = str(card_number).replace("-", "").replace(" ", "")
    return f"XXXX-XXXX-XXXX-{clean_card[-4:]}"


# 3. National ID / SSN Masking (Keep only last 3 digits)
def mask_nid(national_id):
    clean_id = str(national_id).replace("-", "")
    return f"***-**-{clean_id[-3:]}"


# 4. SHA-256 Health Tokenizer (HIPAA Safe Harbor)
def generate_health_token(name, record_id):
    raw_str = f"{name}_{record_id}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()[:16]


# Main Data Generation Function
def create_synthetic_dataset(num_rows=100):
    records = []
    diagnoses = [
        "Hypertension",
        "Type 2 Diabetes",
        "Viral Fever",
        "Asthma",
        "Migraine",
        "Seasonal Allergy",
        "General Checkup",
    ]

    print(
        f"[*] Generating {num_rows} synthetic records with GDPR/HIPAA masking..."
    )

    for i in range(1, num_rows + 1):
        raw_name = fake.name()
        raw_email = fake.email()
        raw_phone = fake.phone_number()
        raw_card = fake.credit_card_number()
        raw_nid = fake.ssn()
        raw_diagnosis = fake.random_element(diagnoses)

        record = {
            "Customer_ID": f"CUST-2026-{i:04d}",
            "Synthetic_Name": raw_name,
            "Masked_Email": mask_email(raw_email),
            "Masked_Phone": raw_phone[:6] + "XXXXXX",
            "City": fake.city(),
            "Country": fake.country(),
            "Masked_Credit_Card": mask_card(raw_card),
            "Masked_NID_SSN": mask_nid(raw_nid),
            "Anonymized_Health_Token": generate_health_token(raw_name, i),
            "Clinical_Diagnosis": raw_diagnosis,
            "Compliance_Standard": "GDPR (Art. 32) & HIPAA Verified",
        }
        records.append(record)

    df = pd.DataFrame(records)
    output_csv = "synthetic_customer_dataset_gdpr_hipaa.csv"
    df.to_csv(output_csv, index=False)
    print(f"[+] Success! Dataset saved to: {output_csv} ({len(df)} rows)")
    return df


if __name__ == "__main__":
    df_result = create_synthetic_dataset(100)
    print("\n--- First 5 Generated Records Preview ---")
    print(
        df_result[
            [
                "Customer_ID",
                "Synthetic_Name",
                "Masked_Email",
                "Masked_Credit_Card",
                "Masked_NID_SSN",
            ]
        ].head()
    )