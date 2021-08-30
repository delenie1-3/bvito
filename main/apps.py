from django.apps import AppConfig

from django.dispatch import Signal
from .utilities import send_activation_notification

class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Объявления BVITO'#название проекта в разработке

user_registered = Signal(providing_args=['instance'])

def user_registered_dispatcher(sender, **kwargs):#рассылка электронных писем
    send_activation_notification(kwargs['instance'])

user_registered.connect(user_registered_dispatcher)