from django.urls import path
from .views import PaymentHandler, WebHookHandler

urlpatterns = [
    path('', PaymentHandler.as_view()),
    path('webhook/', WebHookHandler.as_view()),
]