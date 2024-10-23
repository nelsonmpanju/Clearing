app_name = "clearing"
app_title = "Clearing"
app_publisher = "Nelson Mpanju"
app_description = "Clearing and Forwarding"
app_email = "nelsonnorbert87@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/clearing/css/clearing.css"
# app_include_js = "/assets/clearing/js/clearing.js"

# include js, css files in header of web template
# web_include_css = "/assets/clearing/css/clearing.css"
# web_include_js = "/assets/clearing/js/clearing.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "clearing/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "clearing.utils.jinja_methods",
# 	"filters": "clearing.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "clearing.install.before_install"
# after_install = "clearing.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "clearing.uninstall.before_uninstall"
# after_uninstall = "clearing.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "clearing.utils.before_app_install"
# after_app_install = "clearing.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "clearing.utils.before_app_uninstall"
# after_app_uninstall = "clearing.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "clearing.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "TRA Clearance": {
        "on_submit": "clearing.clearing.doctype.clearing_file.clearing_file.update_status_to_cleared"
    },
    "Shipment Clearance": {
        "on_submit": "clearing.clearing.doctype.clearing_file.clearing_file.update_status_to_cleared"
    },
    "Physical Verification": {
        "on_submit": "clearing.clearing.doctype.clearing_file.clearing_file.update_status_to_cleared"
    },
    "Port Clearance": {
        "on_submit": "clearing.clearing.doctype.clearing_file.clearing_file.update_status_to_cleared"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"clearing.tasks.all"
# 	],
# 	"daily": [
# 		"clearing.tasks.daily"
# 	],
# 	"hourly": [
# 		"clearing.tasks.hourly"
# 	],
# 	"weekly": [
# 		"clearing.tasks.weekly"
# 	],
# 	"monthly": [
# 		"clearing.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "clearing.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "clearing.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "clearing.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["clearing.utils.before_request"]
# after_request = ["clearing.utils.after_request"]

# Job Events
# ----------
# before_job = ["clearing.utils.before_job"]
# after_job = ["clearing.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"clearing.auth.validate"
# ]
fixtures = [
    {
        "dt": "Clearing Document Type",
        "filters": [
            [
                "name", "in", [
                    "Import Duty Payment Receipt",
                    "Import Declaration",
                    "Inspection Certificate",
                    "Health Certificate",
                    "Phytosanitary Certificate",
                    "Letter of Credit (LC)",
                    "Import License",
                    "Packing List",
                    "Bill of Lading B/L",
                    "Air Waybill (AWB)",
                    "Delivery Order",
                    "Insurance Certificate",
                    "Certificate of Origin",
                    "Payment Note",
                    "Bank Document",
                    "Commercial Invoice",
                    "Assessment Document",
                    "Tanzania Bureau Of Standards - Debit Advice",
                    "Pre-Export Verification of Conformity (PVoC)"
                ]
            ]
        ]
    },
    {
        "dt": "Item",
        "filters": [
            [
                "name", "in", [
                    "Port Clearance",
                    "Shipment Clearance",
                    "TRA Clearance",
                    "Physical Verification"
                ]
            ]
        ]
    }
]