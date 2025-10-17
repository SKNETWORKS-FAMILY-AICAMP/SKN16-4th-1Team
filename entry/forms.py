from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
    validate_password,
)


class AddForm(forms.Form):

    productivity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'type': 'range',
                'min': '0',
                'max': '10',
                'value': '5',
                'step': '1',
                'class': 'mb-3 form-control'
            }
        ),
        label="Rate Today's Productivity",
        required=True
    )

    note = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name this day (anything you like)',
                'class': 'form-control mb-3',
            }
        ),
        label='',
        required=True
    )

    content = forms.CharField(
        widget=forms.Textarea(
            {
                'placeholder': 'Write what you feel...',
                'class': 'form-control quilljs-textarea',
                'rows': '15'
            }
        ),
        label='',
        required=True
    )

    image_url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'placeholder': 'Preview image URL',
                'class': 'form-control mb-3'
            }
        ),
        label='Diary Image',
        required=False,
        help_text='Enter the preview image URL if you have one.'
    )


class SignupForm(forms.Form):
    email = forms.EmailField(
        label='이메일(ID)',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validators_help_text_html(),
    )
    name = forms.CharField(
        label='이름',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    nickname = forms.CharField(
        label='닉네임',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    error_messages = {
        'duplicate_email': '이미 사용 중인 이메일입니다.',
    }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        user_model = get_user_model()
        if user_model.objects.filter(username__iexact=email).exists() or user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.error_messages['duplicate_email'])
        return email

    def save(self):
        user_model = get_user_model()
        email = self.cleaned_data['email'].strip().lower()
        password = self.cleaned_data['password']
        name = self.cleaned_data['name']
        nickname = self.cleaned_data['nickname']

        user = user_model.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.first_name = name
        user.last_name = nickname
        user.save(update_fields=['first_name', 'last_name'])
        return user

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get('class', '')
            classes = css_class.split()
            if 'form-control' not in classes:
                classes.append('form-control')
            field.widget.attrs['class'] = ' '.join(classes).strip()
        self.fields['username'].label = '이메일(ID)'
        username_widget = forms.EmailInput(attrs=self.fields['username'].widget.attrs)
        self.fields['username'].widget = username_widget
        self.fields['password'].label = '비밀번호'
