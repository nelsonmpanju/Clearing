# Clearing Document Python Script for ERPNext
# © 2024, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ClearingDocument(Document):
    def after_insert(self):
        populate_document_in_parent(self)

def populate_document_in_parent(self):
    parent_doctype_map = {
        "Clearing File": {
            "doctype": "Clearing File",
            "child_table": "document",  
            "link_field": "clearing_file"
        },
        "Physical Verification": {
            "doctype": "Physical Verification",
            "child_table": "document",  
            "link_field": "clearing_file"
        },
        "TRA Clearance": {
            "doctype": "TRA Clearance",
            "child_table": "document",  
            "link_field": "clearing_file"  
        },
        "Port Clearance": {
            "doctype": "Port Clearance",
            "child_table": "document",  
            "link_field": "clearing_file"  
        },
        "Shipment Clearance": {
            "doctype": "Shipment Clearance",
            "child_table": "document", 
            "link_field": "clearing_file"  
        }
    }

    # Find the parent configuration
    parent_config = parent_doctype_map.get(self.linked_file)

    if not parent_config:
        frappe.throw(f"No valid parent document configuration found for '{self.linked_file}'")

    # Get the parent document based on whether it's a "Clearing File" or another type
    if self.linked_file == "Clearing File":
        parent_doc = frappe.get_doc(parent_config['doctype'], self.clearing_file)
    else:
        parent_doc = frappe.get_doc(parent_config['doctype'], {parent_config['link_field']: self.clearing_file})

    # Check if the parent document has the child table field
    if not parent_doc.meta.has_field(parent_config['child_table']):
        frappe.throw(f"The child table '{parent_config['child_table']}' does not exist in '{parent_config['doctype']}'.")

    # Construct document attributes string from the clearing document attributes
    document_attributes = "" 
    for row in self.clearing_document_attributes:
        attribute = row.document_attribute
        value = row.document_attribute_value
        if attribute and value:
            document_attributes += f"{attribute}: {value}\n"

    # Look for an existing document entry in the child table
    existing_entry = None
    for entry in parent_doc.get(parent_config['child_table']):
        # frappe.throw(str(entry))
        if entry.document_name == self.document_type and entry.clearing_document_id == self.name:
            existing_entry = entry
            break

    # Update the existing entry or append a new one
    if existing_entry:
        existing_entry.document_received = self.get("document_received", 1)
        existing_entry.clearing_document_id = self.name
        existing_entry.view_document = self.document_attachment
        existing_entry.submission_date = self.get("submission_date", frappe.utils.now_datetime())
        existing_entry.document_attributes = document_attributes
        frappe.msgprint(f"Document {self.document_type} in {parent_config['doctype']} updated successfully.")
    else:
        document_entry = {
            "document_name": self.document_type,
            "view_document": self.document_attachment,
            "document_received": self.get("document_received", 1),
            "clearing_document_id": self.name,
            "submission_date": self.get("submission_date", frappe.utils.now_datetime()),
            "document_attributes": document_attributes,
            "parent": self.clearing_file  # Ensure it's linked to the correct clearing file
        }
        parent_doc.append(parent_config['child_table'], document_entry)
        frappe.msgprint(f"Document {self.document_type} appended to {parent_config['doctype']}.")

    # Save the parent document after the updates
    parent_doc.save()
