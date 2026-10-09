"""
Single source of truth for the Retail Outlet Inspection Intelligence Assistant
dataset schema and controlled vocabularies.

Every downstream module -- ingestion, validation, compliance metrics, risk
scoring, the OpenAI layer, and the Streamlit dashboard -- should import from
here rather than hardcoding column names or allowed values. If a controlled
value ever changes (e.g. a new follow_up_status is introduced), this is the
only file that should need to change.
"""




from numpy import single


SHEET_INSPECTION_RECORDS = "INSPECTION_RECORDS"
SHEET_OUTLET_DIRECTORY = "OUTLET_DIRECTORY"
SHEET_CATEGORY_REFERENCE = "CATEGORY_REFERENCE"
SHEET_DATA_DICTIONARY = "DATA_DICTIONARY"





INSPECTION_RECORDS_COLUMNS = {
    "inspection_id",
    "outlet_id",
    "outlet_name",
    "location",
    "lga",
    "outlet_type",
    "inspection_date",
    "inspection_type",
    "inspection_category",
    "observation",
    "compliance_status",
    "severity",
    "recommended_action",
    "follow_up_status",
    "resolution_date",
    "inspector_name",
    "days_to_resolution",
    "record_source",
}

OUTLET_DIRECTORY_COLUMNS = {
    "outlet_id": "string",
    "outlet_name": "string",
    "location": "string",
    "lga": "string",
    "outlet_type": "string",
    "operational_status": "string",
}

CATEGORY_REFERENCE_COLUMNS = {
    "inspection_category": "string",
    "description": "string",
    "example_compliant_observation": "string",
    "example_non_compliant_observation": "string",
}


DATA_DICTIONARY_COLUMNS = {
    "column": "string",
    "description": "string",
    "data_type": "string",
    "permitted_values": "string",
}




#single source of truth for the Retail Outlet Inspection Intelligence Assistant
#dataset schema and controlled vocabularies.


COMPLIANCE_STATUS_VALUES = {"Compliant", "Non-Compliant"}

SEVERITY_VALUES = {"Not Applicable", "Low", "Medium", "High", "Critical"}

FOLLOW_UP_STATUS_VALUES = {"Open", "In Progress", "Resolved", "Overdue", "Not Required"}

INSPECTION_TYPE_VALUES = {"Routine", "Follow-up", "Spot Check", "Complaint-Based"}

OUTLET_TYPE_VALUES = {"Company-Owned", "Dealer-Operated", "Franchise"}

OPERATIONAL_STATUS_VALUES = {"Active", "Temporarily Closed"}

INSPECTION_CATEGORIES = [
    "Product Availability",
    "Product Display and Labelling",
    "Pricing Compliance",
    "Storage Conditions",
    "Housekeeping and Organization",
    "Safety Equipment Availability",
    "Documentation and Records",
    "Equipment Condition",
    "Signage and Branding",
    "Staff Practices",
    "Customer-Facing Conditions",
    "General Outlet Condition",
]