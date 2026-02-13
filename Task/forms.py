from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task
from django.contrib.auth.forms import AuthenticationForm


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "e.g. Finish UI improvements",
                "class": "form-input"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Optional notes...",
                "class": "form-input"
            }),
            "due_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-input"
            }),
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove noisy help text
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        # Apply smooth styling
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-input"
            })




class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply the same smooth UI styling
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-input"
            })

        # Optional placeholders (makes UX nicer)
        self.fields["username"].widget.attrs.update({
            "placeholder": "Your username"
        })
        self.fields["password"].widget.attrs.update({
            "placeholder": "Your password"
        })
