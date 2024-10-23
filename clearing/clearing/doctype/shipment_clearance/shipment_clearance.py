# Copyright (c) 2024, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from clearing.clearing.doctype.port_clearance.port_clearance import ensure_all_documents_attached

class ShipmentClearance(Document):

    def before_save(self):
        """Before saving the document, check if invoice is paid and update the status."""
        if self.invoice_paid:
            # If the invoice is paid, automatically set the status to 'Payment Completed'
            self.status = "Payment Completed"
        else:
            # Reset the status if invoice is not paid
            self.status = "Payment Pending"

        # Check if Delivery Order is attached and validate the Delivery Order Expire Date
        self.check_delivery_order()

    def before_submit(self):
        """Ensure that all required documents are attached and invoice is paid before submission."""
        # This function will check all required documents
        ensure_all_documents_attached(self, "Shipment_clearance_document")

        # Validate payment status before submission
        self.validate_payment_status()

    def validate_payment_status(self):
        """Ensure payment status is 'Payment Completed' before submission."""
        if self.status != "Payment Completed":
            frappe.throw(_("You cannot complete Shipment Clearance unless the payment status is 'Payment Completed'."))

    def check_delivery_order(self):
        """Check if Delivery Order is attached and make sure Delivery Order Expire Date is set."""
        for row in self.document:
            if row.document_name == "Delivery Order":
                if not self.delivery_order_expire_date:
                    frappe.throw(_("Please set the Delivery Order Expire Date before saving."))
