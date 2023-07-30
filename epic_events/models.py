from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    company_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'ID {self.id} - Client {self.full_name} - {self.company_name} - {self.email}'


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    commercial_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Contract {self.id} with client {self.client.full_name}'


class Event(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, related_name='events', on_delete=models.SET_NULL, null=True)
    event_date_start = models.DateTimeField()
    event_date_end = models.DateTimeField()
    location = models.TextField()
    attendees = models.IntegerField()
    notes = models.TextField()
    event_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.event_name} (Event ID: {self.id}) for contract {self.contract.id}'

    @property
    def client_name(self):
        return self.contract.client.full_name

    @property
    def client_contact_email(self):
        return self.contract.client.email

    @property
    def client_contact_phone(self):
        return self.contract.client.phone
