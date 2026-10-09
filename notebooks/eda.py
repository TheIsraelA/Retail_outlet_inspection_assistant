# %%
import sys 
sys.path.insert(0, r"C:\RetailSens")
import pandas as pd
import matplotlib.pyplot as plt

from ingestion.load_data import load_dataset

ds = load_dataset()
records = ds.records

#%%
#Overall Compliance rate
compliance_counts = records["compliance_status"].value_counts(normalize=True)
print(compliance_counts)

# %%
# Compliance rate by inspection category
category_compliance = (
    records.groupby("inspection_category")["compliance_status"]
    .apply(lambda s: (s == "Non-Compliant").mean())
    .sort_values(ascending=False)
)
print(category_compliance)

category_compliance.plot(kind="barh", figsize=(8, 6), title="Non-Compliance Rate by Category")
plt.xlabel("Non-Compliance Rate")
plt.tight_layout()
plt.show()

# %%
# Severity mix, non-compliant records only
non_compliant = records[records["compliance_status"] == "Non-Compliant"]
severity_mix = non_compliant["severity"].value_counts(normalize=True)
print(severity_mix)

# %%
# Outlet-level non-compliance rate — worst 10 outlets
outlet_compliance = (
    records.groupby(["outlet_id", "outlet_name"])["compliance_status"]
    .apply(lambda s: (s == "Non-Compliant").mean())
    .sort_values(ascending=False)
)
print(outlet_compliance.head(10))

# %%
# Location / LGA breakdown
lga_compliance = (
    records.groupby("lga")["compliance_status"]
    .apply(lambda s: (s == "Non-Compliant").mean())
    .sort_values(ascending=False)
)
print(lga_compliance)


