from django.contrib import admin
from .models import Customer, Owner, Room, Service, Order, Sale, QuestBook, Event


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['identification', 'rooms', 'beds']

admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(Room, ApartmentAdmin)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Sale)
admin.site.register(QuestBook)
admin.site.register(Event)
