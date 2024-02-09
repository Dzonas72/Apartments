from django.urls import path
from .views import room_view, rooms, add_room, update_room, customers, sales, services, orders, add_customer, \
    add_service, delete_room, delete_customer, add_order, count_customer_payed_money, CalendarView, event, \
    update_customer, update_order, update_service, confirm_event
from django.conf.urls.static import static
from django.conf import settings


app_name = "apartment"

urlpatterns = [
    # rooms path
    path("", rooms, name="rooms"),
    path("room/<int:pk>", room_view, name="room"),
    path("add", add_room, name="room_add"),
    path("delete_room/<int:room_id>", delete_room, name="room_delete"),
    path("room/<int:pk>/update", update_room, name='room_update'),
    # calendar path
    path("room_calendar", CalendarView.as_view(), name="calendar_view"),
    # customers path
    path("customers", customers, name="customers"),
    path("add_customer", add_customer, name="customer_add"),
    path("delete_customer/<int:customer_id>", delete_customer, name="customer_delete"),
    path("update_customer/<int:pk>", update_customer, name="customer_update"),
    path("customers_payed/<int:customer_id>", count_customer_payed_money, name="customers_payed_money"),
    # sales path
    path("sale", sales, name="sale"),
    # sales path
    path("service", services, name="service"),
    path("add_service", add_service, name="service_add"),
    path("update_service/<int:service_id>", update_service, name="service_update"),
    # orders path
    path("orders", orders, name="orders"),
    path("add_order", add_order, name="order_add"),
    path("update_order/<int:event_id>", update_order, name="order_update"),
    # event path
    path("room_calendar_event", event, name="event"),
    path("room_calendar_event/<int:event_id>", event, name="event_update"),
    path("confirm_event", confirm_event, name="event_confirmation"),
]

urlpatterns += static(settings.STATIC_URL, document_rout=settings.STATIC_ROOT)
