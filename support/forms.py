from django import forms

class NewTicketForm(forms.Form):
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly':'readonly'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
