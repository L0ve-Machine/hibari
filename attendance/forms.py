from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student_class','name','status']
        widgets = {
            'student_class': forms.Select(attrs={'class':'form-select'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'名前'}),
            'status': forms.Select(attrs={'class':'form-select'}),
        }

class PasswordForm(forms.Form):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))