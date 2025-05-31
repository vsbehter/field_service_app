frappe.ui.form.on('Work Order', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.estimate_approved && !frm.doc.invoice_created) {
            frm.add_custom_button('Создать Invoice', () => {
                frappe.call({
                    method: 'field_service_app.field_service.doctype.work_order.work_order.create_invoice_from_work_order',
                    args: {
                        work_order_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint('Invoice создан: <a href="/app/sales-invoice/' + r.message + '"><b>' + r.message + '</b></a>');
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    }
});
