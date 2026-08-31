from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше ім'я", widget=forms.TextInput(
        attrs={
            'class': 'form-input',
            'placeholder': "Введіть ваше ім'я"
        }
    ))
    email = forms.EmailField(max_length=100, label="Почта", widget=forms.EmailInput(
        attrs={
            'class': 'form-input',
            'placeholder': "Введіть вашу почту"
        }
    ))
    subject = forms.CharField(max_length=100, label="Тема звернення", widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': "Введіть тему повідомлення"
            }
        ))
    message = forms.CharField(max_length=100, label="Повідомлення", widget=forms.Textarea(
                attrs={
                    'class': 'form-input',
                    'placeholder': "Введіть ваше повідомлення"
                }
            ))