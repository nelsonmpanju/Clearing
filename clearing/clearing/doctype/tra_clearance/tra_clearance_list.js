frappe.listview_settings['TRA Clearance'] = {
    get_indicator(doc) {
            // customize indicator color
            if (doc.status=="Payment Completed") {
                return [__("Payment Completed"), "green", "status,=,Payment Completed"];
            } else {
                return [__("Payment Pending"), "darkgrey", "status,=,Payment Pending"];
            }
        },
}