# Copyright (c) 2024, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from clearing.clearing.doctype.port_clearance.port_clearance import ensure_all_documents_attached

class PhysicalVerification(Document):
    
    def before_save(self):
        """Before saving the document, check if invoice is paid and update the status."""
        if self.invoice_paid:
            # If the invoice is paid, automatically set the status to 'Payment Completed'
            self.status = "Payment Completed"
        else:
            # Reset the status if invoice is not paid
            self.status = "Payment Pending"

        # Check release order date and update verification status accordingly
        if self.release_order_date:
            self.verification_status = "Completed"
        else:
            self.verification_status = "Pending"

    def before_submit(self):
        """Ensure all required documents are attached and verification is completed before submission."""
        # Check if all required documents are attached
        ensure_all_documents_attached(self, "physical_verification_document")

        # Ensure verification is marked as completed
        if self.verification_status != "Completed":
            frappe.throw(_("You can't submit unless verification is completed."))


    def validate_status(self):
        """Ensure both payment and verification statuses are completed before submission."""
        if self.status != "Payment Completed":
            frappe.throw(_("You cannot complete Physical Verification unless the payment status is 'Payment Completed'."))

        if self.verification_status != "Completed":
            frappe.throw(_("You cannot complete Physical Verification unless the verification status is 'Completed'."))
