from django.contrib import admin
from .models import Payment, PaymentIntent

# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentIntent)
