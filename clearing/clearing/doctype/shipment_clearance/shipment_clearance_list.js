// frappe.listview_settings['Shipment Clearance'] = {
//     refresh(listview) {
//         // Hook onto the alert container and log its content
//         const alertContainer = document.getElementById('alert-container');
//         if (alertContainer) {
//             const alertContent = alertContainer.innerHTML;
//             console.log('Alert Container Content:', alertContent);
//         }

//         // Fetch the user's desk theme
//         frappe.call({
//             method: "frappe.client.get_value",
//             args: {
//                 doctype: "User",
//                 fieldname: "desk_theme",
//                 filters: { name: frappe.session.user }
//             },
//             callback: function(r) {
//                 if (r.message) {
//                     let deskTheme = r.message.desk_theme;

//                     // Loop through each list row
//                     $(".list-row-container .list-row").each(function (i, obj) {
//                         // Get the document name from the data-name attribute
//                         const docname = $(this).find('a[data-name]').attr('data-name');
//                         if (!docname) return;

//                         // Fetch the document to get the delivery_order_expire_date
//                         frappe.call({
//                             method: "frappe.client.get",
//                             args: {
//                                 doctype: "Shipment Clearance",
//                                 name: docname
//                             },
//                             callback: function(r) {
//                                 if (r.message) {
//                                     const expiryDateText = r.message.delivery_order_expire_date;

//                                     if (!expiryDateText) return;

//                                     // Parse the expiry date using JavaScript's Date object
//                                     const expiryDate = new Date(expiryDateText);
//                                     const today = new Date();

//                                     let backgroundColor = ''; // default to no color

//                                     if (expiryDate < today) {
//                                         backgroundColor = (deskTheme === 'Dark') ? '#451917' : '#bb8277'; // Darker red for dark mode
//                                     } else if (
//                                         expiryDate.getDate() === today.getDate() + 1 &&
//                                         expiryDate.getMonth() === today.getMonth() &&
//                                         expiryDate.getFullYear() === today.getFullYear()
//                                     ) {
//                                         backgroundColor = (deskTheme === 'Dark') ? '#705200' : '#f7ead8'; // Softer yellow for dark mode
//                                     }

//                                     // Apply the background color if necessary
//                                     if (backgroundColor) {
//                                         $(obj).css('background-color', backgroundColor);
//                                     }
//                                 }
//                             }
//                         });
//                     });
//                 }
//             }
//         });
//     }
// };
