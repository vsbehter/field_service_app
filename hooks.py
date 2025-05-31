app_name = "field_service_app"
app_title = "Field Service App"
app_publisher = "Vladimir"
app_description = "Field service workflow for appliance repair"
app_email = "you@example.com"
app_license = "MIT"

# Подключаем JS-файлы, если они реально существуют
app_include_js = [
    "/assets/field_service_app/js/dashboard.js",
    "/assets/field_service_app/js/work_order.js"
]

# Автоматическое создание Work Order при обновлении Call Log
doc_events = {
    "Call Log": {
        "after_insert": "field_service_app.api.work_order.create_work_order_from_call_log"
    }
}

# Подключаем фикстуры, если будут кастомные поля или настройки
fixtures = ["Custom Field", "Property Setter"]
