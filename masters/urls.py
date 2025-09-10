from django.urls import path
from masters import views
app_name = "masters"

urlpatterns = [
    # Country Master
    path('<module>/create/country/',views.create_country,name='create_country'),
    path('<module>/details/country/',views.country_details,name='country_details'),
    path('<module>/update/country/<id>/',views.country_update,name='country_update'),
    path('<module>/delete/country/<id>/',views.country_delete,name='country_delete'),
    
    # State Master
    path('<module>/create/state/',views.create_state,name='create_state'),
    path('<module>/details/state/',views.state_details,name='state_details'),
    path('<module>/update/state/<id>/',views.state_update,name='state_update'),
    path('<module>/delete/state/<id>/',views.state_delete,name='state_delete'),
    
    # Port Master
    path('<module>/create/port/',views.create_port,name='create_port'),
    path('<module>/details/port/',views.port_details,name='port_details'),
    path('<module>/update/port/<id>/',views.port_update,name='port_update'),
    path('<module>/delete/port/<id>/',views.port_delete,name='port_delete'),
    path('popup/ports/<id>/',views.PortCreatePopup,name='PortCreatePopup'),

    
    # Location Master
    path('<module>/create/location/',views.create_location,name='create_location'),
    path('<module>/details/location/',views.location_details,name='location_details'),
    path('<module>/update/location/<id>/',views.location_update,name='location_update'),
    path('<module>/delete/location/<id>/',views.location_delete,name='location_delete'),
    path('popup/location/<id>/',views.LocationCreatePopup,name='LocationCreatePopup'),
    
    # Currency Master
    path('<module>/create/currency/',views.create_currency,name='create_currency'),
    path('<module>/details/currency/',views.currency_details,name='currency_details'),
    path('<module>/update/currency/<id>/',views.currency_update,name='currency_update'),
    path('<module>/delete/currency/<id>/',views.currency_delete,name='currency_delete'),
    
    # Shipping Line Master
    path('<module>/create/shipping/line/',views.create_shippingline,name='create_shippingline'),
    path('<module>/details/shipping/line/',views.shippingline_details,name='shippingline_details'),
    path('<module>/update/shipping/line/<id>/',views.shippingline_update,name='shippingline_update'),
    path('<module>/delete/shipping/line/<id>/',views.shippingline_delete,name='shippingline_delete'),
    
    
    # Air Line Master
    path('<module>/create/air/line/',views.create_airline,name='create_airline'),
    path('<module>/details/air/line/',views.airline_details,name='airline_details'),
    path('<module>/update/air/line/<id>/',views.airline_update,name='airline_update'),
    path('<module>/delete/air/line/<id>/',views.airline_delete,name='airline_delete'),

    # Party
    path('<module>/create/party/',views.create_party,name='create_party'),
    path('<module>/details/party/',views.party_details,name='party_details'),
    path('<module>/update/party/<id>/',views.party_update,name='party_update'),
    path('<module>/delete/party/<id>/',views.party_delete,name='party_delete'),
    path('<module>/tally/party/<id>/',views.party_to_tally,name='party_to_tally'),
    
    # Party Master
    path('<module>/create/party-adress/',views.create_party_address,name='create_party_address'),
    path('<module>/details/party-adress/',views.party_address_details,name='party_address_details'),
    path('<module>/update/party-adress/<id>/',views.party_address_update,name='party_address_update'),
    path('<module>/delete/party-adress/<id>/',views.party_address_delete,name='party_address_delete'),

    
    # Vendor
    path('<module>/create/vendor/',views.create_vendor,name='create_vendor'),
    path('<module>/details/vendor/',views.vendor_details,name='vendor_details'),
    path('<module>/update/vendor/<id>/',views.vendor_update,name='vendor_update'),
    path('<module>/delete/vendor/<id>/',views.vendor_delete,name='vendor_delete'),
    
    
    
    # Commodity
    path('<module>/commodity/create/',views.create_commodity,name='create_commodity'),
    path('<module>/commodity/details/',views.commodity_details,name='commodity_details'),
    path('<module>/update/commodity/<id>/',views.commodity_update,name='commodity_update'),
    path('<module>/delete/commodity/<id>/',views.commodity_delete,name='commodity_delete'),
    
    # Billing Head
    path('<module>/billing/head/create/',views.create_billing_head,name='create_billing_head'),
    path('<module>/billing/head/details/',views.billing_head_details,name='billing_head_details'),
    path('<module>/update/billing/head/<id>/',views.billing_head_update,name='billing_head_update'),
    path('<module>/delete/billing/head/<id>/',views.billing_head_delete,name='billing_head_delete'),
    path('<module>/tally/billing/head/<id>/',views.billing_head_to_tally,name='billing_head_to_tally'),
    
    
    # Bank
    path('<module>/bank/create/',views.create_bank,name='create_bank'),
    path('<module>/bank/details/',views.bank_details,name='bank_details'),
    path('<module>/update/bank/<id>/',views.bank_update,name='bank_update'),
    path('<module>/delete/bank/<id>/',views.bank_delete,name='bank_delete'),
    
    # UOM
    path('<module>/uom/create/',views.create_uom,name='create_uom'),
    path('<module>/uom/details/',views.uom_details,name='uom_details'),
    path('<module>/update/uom/<id>/',views.uom_update,name='uom_update'),
    path('<module>/delete/uom/<id>/',views.uom_delete,name='uom_delete'),
    path('<module>/tally/uom/<id>/',views.uom_to_tally,name='uom_to_tally'),
    
    # Battery
    path('<module>/battery/create/',views.create_battery,name='create_battery'),
    path('<module>/battery/details/',views.battery_details,name='battery_details'),
    path('<module>/update/battery/<id>/',views.battery_update,name='battery_update'),
    path('<module>/delete/battery/<id>/',views.battery_delete,name='battery_delete'),
    
    # Tyre
    path('<module>/tyre/create/',views.create_tyre,name='create_tyre'),
    path('<module>/tyre/details/',views.tyre_details,name='tyre_details'),
    path('<module>/update/tyre/<id>/',views.tyre_update,name='tyre_update'),
    path('<module>/delete/tyre/<id>/',views.tyre_delete,name='tyre_delete'),
    
    # Driver
    path('<module>/driver/create/',views.create_driver,name='create_driver'),
    path('<module>/driver/details/',views.driver_details,name='driver_details'),
    path('<module>/update/driver/<id>/',views.driver_update,name='driver_update'),
    path('<module>/delete/driver/<id>/',views.driver_delete,name='driver_delete'),
    
    # Trailor
    path('<module>/trailor/create/',views.create_trailor,name='create_trailor'),
    path('<module>/trailor/details/',views.trailor_details,name='trailor_details'),
    path('<module>/update/trailor/<id>/',views.trailor_update,name='trailor_update'),
    path('<module>/delete/trailor/<id>/',views.trailor_delete,name='trailor_delete'),
    
    
    # Ledger Category
    path('<module>/ledger-category/create/',views.create_ledger_categories,name='create_ledger_categories'),
    path('<module>/ledger-category/details/',views.ledger_categories_details,name='ledger_categories_details'),
    path('<module>/update/ledger-category/<id>/',views.ledger_categories_update,name='ledger_categories_update'),
    path('<module>/delete/ledger-category/<id>/',views.ledger_categories_delete,name='ledger_categories_delete'),
    
    # Ledger Sub Category
    path('<module>/ledger-sub-category/create/',views.create_ledger_sub_categories,name='create_ledger_sub_categories'),
    path('<module>/ledger-sub-category/details/',views.ledger_sub_categories_details,name='ledger_sub_categories_details'),
    path('<module>/update/ledger-sub-category/<id>/',views.ledger_sub_categories_update,name='ledger_sub_categories_update'),
    path('<module>/delete/ledger-sub-category/<id>/',views.ledger_sub_categories_delete,name='ledger_sub_categories_delete'),
    
    # Ledger Master
    path('<module>/ledger/create/',views.create_ledger,name='create_ledger'),
    path('<module>/ledger/details/',views.ledger_details,name='ledger_details'),
    path('<module>/update/ledger/<id>/',views.ledger_update,name='ledger_update'),
    path('<module>/delete/ledger/<id>/',views.ledger_delete,name='ledger_delete'),
    
    # Category
    path('<module>/category/create/',views.create_category,name='create_category'),
    path('<module>/category/details/',views.category_details,name='category_details'),
    path('<module>/update/category/<id>/',views.category_update,name='category_update'),
    path('<module>/delete/category/<id>/',views.category_delete,name='category_delete'),
    

    # Department
    path('<module>/department/create/',views.create_department,name='create_department'),
    path('<module>/department/detail/',views.department_details,name='department_details'),
    path('<module>/department/update/<id>/',views.department_update,name='department_update'),
    path('<module>/department/delete/<id>/',views.department_delete,name='department_delete'),
    
    # Designation
    path('<module>/designation/create/',views.create_designation,name='create_designation'),
    path('<module>/designation/detail/',views.designation_details,name='designation_details'),
    path('<module>/designation/update/<id>/',views.designation_update,name='designation_update'),
    path('<module>/designation/delete/<id>/',views.designation_delete,name='designation_delete'),
    
    # Employee
    path('<module>/employee/create/',views.create_employee,name='create_employee'),
    path('<module>/employee/detail/',views.employee_details,name='employee_details'),
    path('<module>/employee/update/<id>/',views.employee_update,name='employee_update'),
    path('<module>/employee/delete/<id>/',views.employee_delete,name='employee_delete'),


     # Advance Admin - User
    path('<module>/user/create/',views.create_user,name='create_user'),
    path('<module>/user/list/',views.user_list,name='user_list'),
    path('<module>/user/update/<int:id>/',views.update_user,name='update_user'),
    path('<module>/user/delete/<int:id>/',views.user_delete,name='user_delete'),

    # Company
    path('<module>/company/create/',views.create_company,name='create_company'),
    path('<module>/company/update/<int:id>/',views.update_company,name='update_company'),
    path('<module>/company/delete/<int:id>/',views.company_delete,name='company_delete'),
    path('<module>/company/details/',views.company_details,name='company_details'),
    
    # Upload Master
    path('<module>/upload/documents/',views.upload_master,name='upload_master'),
    
    
]