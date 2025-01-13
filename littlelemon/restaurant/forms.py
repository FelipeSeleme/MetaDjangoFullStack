from django.forms import ModelForm
from .models import Booking


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

# class BookingForm(ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['first_name', 'last_name', 'guest_number', 'reservation_date', 'reservation_slot', 'comment']
#         widgets = {
#             'reservation_date': DateInput(attrs={'type': 'date', 'required': 'true'}),
#             'reservation_slot': Select(attrs={'required': 'true'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Horários disponíveis (10h - 20h)
#         slots = [(i, f"{i}:00") for i in range(10, 21)]
#         self.fields['reservation_slot'].choices = slots
