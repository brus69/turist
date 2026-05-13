from django import forms

from .models import Tour
from .widgets import DateSlotsCalendarWidget


class TourAdminForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = "__all__"
        widgets = {
            "date_slots": DateSlotsCalendarWidget(),
        }
