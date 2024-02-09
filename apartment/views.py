from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic
from .forms import RoomForm, CustomerForm, OrderForm, ServiceForm, EventForm, RoomAvailabilityForm, SaleForm
from apartment.models import Room, Customer, Service, Sale, Event
from datetime import datetime, date, timedelta
from .utils import Calendar
import calendar
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def rooms(request):
    room = Room.objects.all()
    paginator = Paginator(room, 3)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'apartment/rooms.html', {"page_obj": page_obj})


def room_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    context = {'room': room}
    return render(request, "apartment/room.html", context)

@login_required
def customers(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'apartment/customers.html',  {"page_obj": page_obj})

@login_required
def sales(request):
    sale = Sale.objects.all()
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            context = {'sales': sale, 'form': form}
            return render(request, 'apartment/orders.html', context)
    paginator = Paginator(sale, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'apartment/sale.html', {"page_obj": page_obj})

@login_required
def count_customer_payed_money(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    payed_sum = Sale.objects.filter(customer=customer)
    money = sum(money.price for money in payed_sum)
    count_payment = len([money.price for money in payed_sum])
    serv = set(service.service.service_name for service in payed_sum)
    serv = ", ".join(serv)
    context = {'customer': customer, 'money': money, 'count_payment': count_payment, 'services': serv}
    print()
    return render(request, 'apartment/customers_payed.html', context)


def services(request):
    service = Service.objects.all()
    context = {'services': service}
    return render(request, 'apartment/service.html', context)


@login_required
def orders(request, day=None):
    day = date.today()
    all_rooms = Room.objects.all()
    events = Event.objects.all()
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            check_from = request.POST.get('check_from')
            check_till = request.POST.get('check_till')
            events_2 = Event.objects.filter(start_time__lte=check_till, end_time__gte=check_from)
            busy_rooms = set([event.room for event in events_2])
            free_rooms = (set(all_rooms) - busy_rooms)
            context = {'all_rooms': all_rooms, 'busy_rooms': busy_rooms, 'free_rooms': free_rooms, 'form': form, 'events': events}
            return render(request, 'apartment/orders.html', context)
    else:
        form = RoomAvailabilityForm()
    context = {'all_rooms': all_rooms, 'events': events, 'form': form}
    return render(request, 'apartment/orders.html', context)

@login_required
def confirm_event(request, event_id=None, sale_id=None):
    event_instance = Event()
    sale_instance = Sale()
    if event_id:
        event_instance = get_object_or_404(Event, pk=event_id)
    if sale_id:
        sale_instance = get_object_or_404(Sale, pk=sale_id)
    sale_instance.customer = event_instance.customer
    sale_form = SaleForm(request.POST or None, instance=sale_instance)
    if request.POST:
        if sale_form.is_valid():
            sale_form.save()
            return HttpResponseRedirect(reverse('apartment:calendar_view'))
    return render(request, "apartment/order_event_confirm.html", {'sale_form': sale_form})

@login_required
def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("apartment:rooms")
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, "apartment/room_add.html", context)

@login_required
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apartment:customers")
    else:
        form = CustomerForm()
    context = {'form': form}
    return render(request, "apartment/customer_add.html", context)

@login_required
def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apartment:orders")
    else:
        form = OrderForm()
    context = {'form': form}
    return render(request, "apartment/order_add.html", context)

@login_required
def add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apartment:service")
    else:
        form = ServiceForm()
    context = {'form': form}
    return render(request, "apartment/service_add.html", context)

@login_required
def update_room(request, pk):
    instance = Room.objects.get(pk=pk)
    form = RoomForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("apartment:rooms")
    return render(request, 'apartment/room_update.html', {'form': form})

@login_required
def update_customer(request, pk):
    instance = Customer.objects.get(pk=pk)
    form = CustomerForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("apartment:customers")
    return render(request, 'apartment/customer_update.html', {'form': form})

@login_required
def update_order(request, event_id):
    instance = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("apartment:orders")
    return render(request, 'apartment/order_update.html', {'form': form})

@login_required
def update_service(request, service_id):
    instance = Service.objects.get(pk=service_id)
    form = ServiceForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("apartment:service")
    return render(request, 'apartment/service_update.html', {'form': form})

@login_required
def delete_customer(request, customer_id):
    customer_2 = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer = Customer.objects.get(pk=customer_id)
        customer.delete()
        return redirect("apartment:customers")
    context = {'object': customer_id, 'name': 'customer', 'customer_name': customer_2.first_name}
    return render(request, 'apartment/customer_delete.html', context)

@login_required
def delete_room(request, room_id):
    room_2 = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect("apartment:rooms")
    context = {'object': room_id, 'name': 'room', 'room_name': room_2.identification}
    return render(request, 'apartment/room_delete.html', context)

# @login_required
class CalendarView(generic.ListView):
    model = Event
    template_name = 'apartment/room_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

# @login_required
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

# @login_required
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# @login_required
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('apartment:calendar_view'))
    return render(request, 'apartment/room_calendar_event.html', {'form': form})
