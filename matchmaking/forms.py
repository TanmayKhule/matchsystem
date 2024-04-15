# matchmaking/forms.py
from django import forms

class StudentForm(forms.Form):
    student_name = forms.CharField(label='Student GUID', max_length=100)
    threshold = forms.FloatField(initial=0.5, required=False)
