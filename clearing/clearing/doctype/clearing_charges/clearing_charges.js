// Copyright (c) 2024, Nelson Mpanju and contributors
// For license information, please see license.txt

frappe.ui.form.on('Clearing Charges', {
    clearing_file: function(frm) {
        // Clear the child table before fetching new data
        frm.clear_table("charges");
        
        // Fetch charges from related doctypes where 'paid_by_clearing_agent' is checked
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "TRA Clearance",
                filters: {
                    "clearing_file": frm.doc.clearing_file,
                    "paid_by_clearing_agent": 1
                },
                fields: ["total_charges"],
            },
            callback: function(r) {
                if (r.message) {
                    $.each(r.message, function(i, d) {
                        let row = frm.add_child("charges");
                        row.charge_type = "TRA Clearance";
                        row.amount = d.total_charges;
                        frm.refresh_field("charges");
                    });
                }
            }
        });

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Port Clearance",
                filters: {
                    "clearing_file": frm.doc.clearing_file,
                    "paid_by_clearing_agent": 1
                },
                fields: ["total_charges"],
            },
            callback: function(r) {
                if (r.message) {
                    $.each(r.message, function(i, d) {
                        let row = frm.add_child("charges");
                        row.charge_type = "Port Clearance";
                        row.amount = d.total_charges;
                        frm.refresh_field("charges");
                    });
                }
            }
        });

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Shipment Clearance",
                filters: {
                    "clearing_file": frm.doc.clearing_file,
                    "paid_by_clearing_agent": 1
                },
                fields: ["total_charges"],
            },
            callback: function(r) {
                if (r.message) {
                    $.each(r.message, function(i, d) {
                        let row = frm.add_child("charges");
                        row.charge_type = "Shipment Clearance";
                        row.amount = d.total_charges;
                        frm.refresh_field("charges");
                    });
                }
            }
        });

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Physical Verification",
                filters: {
                    "clearing_file": frm.doc.clearing_file,
                    "paid_by_clearing_agent": 1
                },
                fields: ["total_charges"],
            },
            callback: function(r) {
                if (r.message) {
                    $.each(r.message, function(i, d) {
                        let row = frm.add_child("charges");
                        row.charge_type = "Physical Verification";
                        row.amount = d.total_charges;
                        frm.refresh_field("charges");
                    });
                }
            }
        });
    },

    generate_invoice: function(frm) {
        // Check if there are items in the child table
        if (frm.doc.charges && frm.doc.charges.length > 0) {
            
            // Prepare items for the Sales Invoice
            let items = [];
            frm.doc.charges.forEach(function(row) {
                items.push({
                    item_code: row.charge_type,
                    qty: row.quantity || 1,
                    rate: row.amount,
                    amount: row.amount
                });
            });

            // Create a new Sales Invoice
            frappe.call({
                method: "frappe.client.insert",
                args: {
                    doc: {
                        doctype: "Sales Invoice",
                        customer: frm.doc.consigee,  
                        items: items,
                        posting_date: frappe.datetime.nowdate()
                    }
                },
                callback: function(r) {
                    if (r.message) {
                        // Link the created Sales Invoice to the Clearing Charges
                        frm.set_value('invoice_number', r.message.name);
                        frm.save();
                        frappe.msgprint(__('Sales Invoice {0} created successfully.', [r.message.name]));
                    }
                }
            });
        } else {
            frappe.msgprint(__('Please add charges to create an invoice.'));
        }
    }
});
