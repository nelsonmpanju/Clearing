import frappe
from frappe.model.document import Document
from frappe import _
from clearing.clearing.doctype.port_clearance.port_clearance import ensure_all_documents_attached


class TRAClearance(Document):
    
    def before_save(self):

        
        """Before saving the document, check if invoice is paid and update the status."""
        if self.invoice_paid:
            # If the invoice is paid, automatically set the status to 'Payment Completed'
            self.status = "Payment Completed"
        else:
            # Reset the status if invoice is not paid (you can customize this logic)
            self.status = "Payment Pending"

        
    def before_submit(self):
        # Ensure all required documents are attached before submission
        ensure_all_documents_attached(self, "tra_clearance_document")
        
        # Validate that the invoice is paid and status is set correctly
        self.validate_payment_status()
    
    def validate_payment_status(self):
        """Ensure payment status is marked as 'Payment Completed' before submission."""
        if self.status != "Payment Completed":
            frappe.throw(_("You cannot Complete TRA Clearance unless the Payment Completed."))
