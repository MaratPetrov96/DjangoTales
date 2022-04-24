from .models import *
from django.forms import *
from django.conf import settings

class TaleForm(ModelForm):
    class Meta:
        model = Tale
        fields = ['title','content']
