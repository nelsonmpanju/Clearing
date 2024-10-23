# Copyright (c) 2024, Nelson Mpanju and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ClearingCharges(Document):
    def before_save(self):
        self.fetch_total_charges()

    def fetch_total_charges(self):
        # Initialize total variables
        tra_total = 0
        port_total = 0
        shipment_total = 0
        physical_total = 0
        
        # Fetch charges from the child table
        for charge in self.charges:
            if charge.charge_type == "TRA Clearance":
                tra_total += float(charge.amount)
            elif charge.charge_type == "Port Clearance":
                port_total += float(charge.amount)
            elif charge.charge_type == "Shipment Clearance":
                shipment_total += float(charge.amount)
            elif charge.charge_type == "Physical Verification":
                physical_total += float(charge.amount)
        
        # Update the doc with fetched totals
        self.tra_clearance_total = tra_total
        self.port_clearance_total = port_total
        self.shipment_clearance_total = shipment_total
        self.physical_clearance_total = physical_total
        
        # Calculate total sum
        self.total_charges_sum = tra_total + port_total + shipment_total + physical_total
