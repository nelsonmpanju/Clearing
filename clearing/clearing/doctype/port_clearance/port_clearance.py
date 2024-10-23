# Copyright (c) 2024, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class PortClearance(Document):

    def before_save(self):
        """Before saving the document, check if invoice is paid and update the status."""
        if self.invoice_paid:
            # If the invoice is paid, automatically set the status to 'Payment Completed'
            self.status = "Payment Completed"
        else:
            # Reset the status if invoice is not paid
            self.status = "Payment Pending"


    def before_submit(self):
        """Ensure all required documents are attached and verification is completed before submission."""
        # Ensure that payment is completed before submission
        if self.status != "Payment Completed":
            frappe.throw(_("You can't submit unless the payment status is 'Payment Completed'."))


        # Check if all required documents are attached
        ensure_all_documents_attached(self, "port_clearance_document")

def ensure_all_documents_attached(self, type):
    """Ensure all required documents for the current mode of transport are attached."""
    # Fetch required documents for the given mode of transport
    required_docs = frappe.db.get_all(
        "Mode of Transport Detail",
        filters={
            "parentfield": type,
            'parent': frappe.db.get_value('Clearing File', self.clearing_file, 'mode_of_transport')
        },
        fields=['clearing_document_type']
    )

    # Convert list of dictionaries into a simple list of document names
    required_doc_names = [doc['clearing_document_type'] for doc in required_docs]

    # Check if each required document is present in the Clearing File's child table 'documents'
    missing_docs = []
    for doc_name in required_doc_names:
        exists = any(doc.document_name == doc_name for doc in self.document)
        if not exists:
            missing_docs.append(doc_name)

    # If documents are missing, prevent submission and show an error
    if missing_docs:
        missing_docs_str = ', '.join(missing_docs)
        frappe.throw(
            _('The following required documents are missing and must be attached before submission: {0}')
            .format(missing_docs_str), frappe.ValidationError
        )
