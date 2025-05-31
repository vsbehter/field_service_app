import frappe

@frappe.whitelist()
def create_work_order_from_call_log(doc, method):
    """Создание Work Order из Call Log"""
    # Логика создания рабочего заказа
    pass