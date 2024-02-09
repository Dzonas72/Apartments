from django import forms
from django.forms import ModelForm, Textarea, DateInput
from apartment.models import Room, Customer, Order, Sale, Service, Event


class UserForm(forms.Form):
    name = forms.CharField(label="name", max_length=30, required=True)
    password = forms.CharField(label="password", required=True)
    lastname = forms.CharField(label="lastname", max_length=20, required=True)
    email = forms.EmailField(label="email", max_length=20, required=True)


class RoomAvailabilityForm(forms.Form):
    check_from = forms.DateField(label='Check from')
    check_till = forms.DateField(label='Check till')


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 5}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "description": Textarea(attrs={"cols": 80, "rows": 5}),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            "description": Textarea(attrs={"cols": 80, "rows": 5}),
        }


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"
        widgets = {
            "description": Textarea(attrs={"cols": 80, "rows": 5}),
        }


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "description": Textarea(attrs={"cols": 80, "rows": 5}),
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
