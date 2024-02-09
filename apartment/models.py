from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    objects = models.Manager()
    DoesNotExist = models.Manager()

    class Meta:
        abstract = True


class Customer(BaseModel):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    age = models.IntegerField(blank=False, default=1)
    phone = models.IntegerField(blank=False, default=1)
    email = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=False)
    rating = models.IntegerField(blank=False, default=1)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.age}, {self.country}, {self.city}, {self.phone}'


class Owner(BaseModel):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=30, blank=False)
    phone = models.IntegerField(blank=False, default=1)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}, {self.phone}'


class Room(BaseModel):
    identification = models.CharField(max_length=30, blank=False)
    rooms = models.IntegerField(default=1, blank=False)
    beds = models.IntegerField(default=1, blank=False)
    property = models.CharField(max_length=30, blank=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/css/images/', default='')
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.identification}, {self.property}'


class Order(BaseModel):
    STATUS = {
        'not_paid': "Order is not paid",
        'ordered': "Order completed",
        'reservation': "Apartment is reserved",
    }
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number_persons = models.IntegerField(default=1, blank=False)
    since = models.DateField("since")
    until = models.DateField("till")
    status = models.CharField(max_length=30, choices=STATUS)


class Service(BaseModel):
    service_name = models.CharField(max_length=30, blank=False, default=None)
    price = models.IntegerField(blank=False, default=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None)
    description = models.CharField(max_length=300, blank=False)


class Sale(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discount = models.IntegerField(default=1, blank=False)
    price = models.IntegerField(default=1, blank=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer.first_name} {self.price}'


class QuestBook(BaseModel):
    feedback = models.TextField(max_length=200, blank=False)
    pub_date = models.DateTimeField("date published")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)


class Event(BaseModel):
    STATUS = {
        'reserved': "Room is reserved, not payed",
        'ordered': "Order is completed",
    }
    status = models.CharField(max_length=30, choices=STATUS, default='order')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    number_persons = models.IntegerField(default=1, blank=False)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()

    @property
    def get_html_url(self):
        url = reverse('apartment:event_update', args=(self.id,))
        url_order = reverse('apartment:orders')
        if self.status == 'reserved':
            value = f'<a style="color:blue;" href="{url}"> {self.room} </a>'
        else:
            value = f'<a style="color:red;" href="{url_order}"> {self.room} </a>'
        return value
