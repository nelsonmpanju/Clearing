from frappe import _

def get_data():
    return {
        "fieldname": "name",  # Primary field for linking
        
        "non_standard_fieldnames": {
            "TRA Clearance": "clearing_file",
            "Physical Verification": "clearing_file",
            "Shipment Clearance": "clearing_file",
            "Port Clearance": "clearing_file",
            "Clearing Document": "clearing_file"
        },
        
        "transactions": [
            {
                "label": _("Clearance Processes"),
                "items": ["TRA Clearance", "Physical Verification", "Shipment Clearance", "Port Clearance"]
            },
            {
                "label": _("Attached Documents"),
                "items": ["Clearing Document"]
            }
        ]
    }
