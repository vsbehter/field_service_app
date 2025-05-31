import frappe
from frappe.model.document import Document

class WorkOrder(Document):
    def validate(self):
        if self.estimate_approved and not self.estimate_amount:
            frappe.throw("Enter Estimate Amount when Estimate is Approved")

@frappe.whitelist()
def create_work_order_from_call_log(doc, method):
    try:
        call_doc = doc  # Уже передан как объект

        # Проверка, существует ли уже заявка по этому звонку
        if frappe.db.exists("Work Order", {"call_log": call_doc.name}):
            return

        # Создание новой заявки
        wo = frappe.get_doc({
            "doctype": "Work Order",
            "customer_name": call_doc.customer_name or call_doc.contact_display or "Unnamed Customer",
            "customer_phone": call_doc.contact_mobile or call_doc.contact_number or "",
            "customer_address": "",
            "scheduled_date": frappe.utils.nowdate(),
            "assigned_technician": "",
            "status": "Planned",
            "call_log": call_doc.name
        })
        wo.insert(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Work Order from Call Log")

@frappe.whitelist()
def create_invoice_from_work_order(work_order_name):
    wo = frappe.get_doc("Work Order", work_order_name)

    if not wo.estimate_amount:
        frappe.throw("Невозможно создать счет без суммы оценки.")

    if wo.invoice_created:
        frappe.throw("Invoice уже создан.")

    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": wo.customer_name,
        "items": [
            {
                "item_name": "Услуги по ремонту",
                "description": f"Работа по заказу {wo.name}",
                "qty": 1,
                "rate": wo.estimate_amount
            }
        ],
        "due_date": frappe.utils.nowdate()
    })

    invoice.insert(ignore_permissions=True)
    invoice.submit()

    # Обновим Work Order
    wo.invoice_created = 1
    wo.save(ignore_permissions=True)

    return invoice.name
