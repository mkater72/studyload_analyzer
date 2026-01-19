from django import forms
from .models import Grade, Subject


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'value', 'date']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'weekly_hours', 'semester']
