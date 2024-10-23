// Copyright (c) 2024, Nelson Mpanju and contributors
// For license information, please see license.txt

frappe.ui.form.on('Port Clearance', {
    refresh: function(frm) {
        // Function to handle the creation or redirection of documents
        const container = document.querySelector('[data-fieldname="attach_documents"]');

        if (container) {
            // Find the button element within the container
            const button = container.querySelector('button');

            // Override the entire class of the button with the new class
            if (button) {
                button.className = 'btn btn-xs btn-default bold btn-primary';
            }
        }

        // Add button to generate CF Delivery Note if the status is "Payment Completed"
        if (frm.doc.status === 'Payment Completed' || frm.doc.docstatus === 0 ) {
            frm.add_custom_button(__('Generate CF Delivery Note'), function() {
                // First, check if a CF Delivery Note already exists for the current clearing file
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "CF Delivery Note",
                        filters: {
                            clearing_file: frm.doc.clearing_file
                        },
                        fields: ["name"]
                    },
                    callback: function(r) {
                        if (r.message && r.message.length > 0) {
                            // If the CF Delivery Note exists, route to it and update the cf_delivery_note field
                            frappe.msgprint(__('CF Delivery Note already exists. Redirecting...'));
                            frappe.set_route('Form', 'CF Delivery Note', r.message[0].name);
        
                            // Update the Port Clearance document to set the CF Delivery Note field
                            frappe.call({
                                method: "frappe.client.set_value",
                                args: {
                                    doctype: "Port Clearance",
                                    name: frm.doc.name,
                                    fieldname: "cf_delivery_note",
                                    value: r.message[0].name
                                },
                                callback: function() {
                                    frm.refresh_field("cf_delivery_note");
                                }
                            });
                        } else {
                            // If it doesn't exist, create a new CF Delivery Note
                            frappe.call({
                                method: "frappe.client.insert",
                                args: {
                                    doc: {
                                        doctype: "CF Delivery Note",
                                        clearing_file: frm.doc.clearing_file,
                                        container_deposit_amount: frm.doc.container_deposit_amount,
                                        posting_date : frappe.datetime.now_date()
                                    }
                                },
                                callback: function(response) {
                                    if (response && response.message) {
                                        frappe.msgprint(__('CF Delivery Note created successfully.'));
                                        // Redirect to the newly created CF Delivery Note
                                        frappe.set_route('Form', 'CF Delivery Note', response.message.name);
        
                                        // Update the Port Clearance document to set the CF Delivery Note field
                                        frappe.call({
                                            method: "frappe.client.set_value",
                                            args: {
                                                doctype: "Port Clearance",
                                                name: frm.doc.name,
                                                fieldname: "cf_delivery_note",
                                                value: response.message.name
                                            },
                                            callback: function() {
                                                frm.refresh_field("cf_delivery_note");
                                            }
                                        });
                                    } else {
                                        frappe.msgprint(__('There was an issue creating the CF Delivery Note.'));
                                    }
                                },
                                error: function(err) {
                                    frappe.msgprint(__('Failed to create CF Delivery Note. Please try again.'));
                                }
                            });
                        }
                    },
                    error: function(err) {
                        frappe.msgprint(__('Failed to check existing CF Delivery Note. Please try again.'));
                    }
                });
            });
        }
                
    },

    attach_documents: function(frm) {
        // Create the dialog for document attachment
        let d = new frappe.ui.Dialog({
            title: 'Attach Clearing Document',
            fields: [
                {
                    label: 'Document Type',
                    fieldname: 'document_type',
                    fieldtype: 'Link',
                    options: 'Clearing Document Type',
                    change: function() {
                        let document_type = d.get_value('document_type');
                        if (document_type) {
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: 'Clearing Document Type',
                                    name: document_type
                                },
                                callback: function(r) {
                                    if (r.message && r.message.clearing_document_attribute) {
                                        let attributes_table = d.get_field('document_attributes').grid;
                                        attributes_table.df.data = []; // Clear existing data
                                        attributes_table.refresh();

                                        // Populate table with attributes
                                        r.message.clearing_document_attribute.forEach(aattribute => {
                                            d.fields_dict.document_attributes.df.data.push({
                                                attribute: aattribute.document_attribute,
                                                mandatory: aattribute.mandatory,
                                                value: ''
                                            });
                                        });
                                        attributes_table.refresh();
                                    } else {
                                        frappe.msgprint(__('No attributes found for the selected document type.'));
                                    }
                                },
                                error: function(err) {
                                    console.error('Error fetching document type attributes:', err);
                                    frappe.msgprint(__('Failed to retrieve document attributes. Please try again.'));
                                }
                            });
                        }
                    }
                },
                {
                    fieldname: "attach_document",
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Attach Document',
                    fieldname: "attach_document",
                    fieldtype: 'Attach'
                },
                {
                    fieldname: "attach_document",
                    fieldtype: 'Section Break'
                },
                {
                    label: 'Document Attributes',
                    fieldname: 'document_attributes',
                    fieldtype: 'Table',
                    options: 'Clearing Document Attribute',
                    fields: [
                        { fieldname: 'attribute', label: 'Attribute', fieldtype: 'Data', in_list_view: 1 },
                        { fieldname: 'value', label: 'Value', fieldtype: 'Data', in_list_view: 1 },
                        { fieldname: 'mandatory', label: 'Mandatory', fieldtype: 'Check', in_list_view: 1, read_only: 1 }
                    ]
                }
            ],
            size: 'large',
            primary_action_label: 'Submit',
            primary_action(values) {
                let attachment_url = document.querySelector('.attached-file-link').getAttribute('href');
    
                // Validate attributes before submitting
                let invalid = false;
                values.document_attributes.forEach(attr => {
                    if (attr.mandatory && !attr.value) {
                        invalid = true;
                        frappe.msgprint({
                            title: __('Missing Value'),
                            message: `Please fill the value for ${attr.attribute} as it is mandatory.`,
                            indicator: 'red'
                        });
                    }
                });
    
                if (invalid) return;  // Stop submission if invalid data
    
                let clearing_document_attributes = values.document_attributes.map(attr => ({
                    document_attribute: attr.attribute,
                    document_attribute_value: attr.value,
                    mandatory: attr.mandatory
                }));

                // Create Clearing Document
                frappe.call({
                    method: "frappe.client.insert",
                    args: {
                        doc: {
                            doctype: "Clearing Document",
                            clearing_file: frm.doc.clearing_file,
                            document_attachment: attachment_url,
                            clearing_document_type: values.document_type,
                            linked_file: 'Port Clearance',
                            document_type: values.document_type,
                            clearing_document_attributes: clearing_document_attributes  // Handle child table
                        }
                    },
                    callback: function(response) {
                        if (response && response.message) {
                            frappe.msgprint(__('Clearing Document created successfully.'));
                            d.hide();
                        } else {
                            frappe.msgprint(__('There was an issue creating the Clearing Document. Please try again.'));
                        }
                    },
                    error: function(err) {
                        frappe.msgprint(__('Failed to create Clearing Document. Please try again.'));
                    }
                });
            }
        });
    
        d.show();
    }
});
