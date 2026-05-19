from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Client, Part, Review, Sale, phone_validator, validate_adult


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=80, label='Имя')
    last_name = forms.CharField(max_length=80, label='Фамилия')
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    phone = forms.CharField(max_length=20, label='Телефон', help_text='+375 (29) XXX-XX-XX', validators=[phone_validator])
    email = forms.EmailField(label='Email')
    address = forms.CharField(max_length=220, label='Адрес')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'phone', 'email', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        max_birth_date = today.replace(year=today.year - 18)
        self.fields['birth_date'].widget.attrs['max'] = max_birth_date.isoformat()

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_adult(birth_date)
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                birth_date=self.cleaned_data['birth_date'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                address=self.cleaned_data['address'],
            )
        return user


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = (
            'sku',
            'name',
            'product_type',
            'manufacturer',
            'price',
            'quantity',
            'description',
            'image_url',
            'is_active',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'text')
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4, 'minlength': 10}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('part', 'quantity')
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client')
        super().__init__(*args, **kwargs)
        self.fields['part'].queryset = Part.objects.filter(is_active=True, quantity__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        part = cleaned_data.get('part')
        quantity = cleaned_data.get('quantity')
        if part and quantity and quantity > part.quantity:
            raise ValidationError('На складе нет такого количества товара.')
        return cleaned_data

    def save(self, commit=True):
        sale = super().save(commit=False)
        sale.client = self.client
        sale.unit_price = sale.part.price
        if commit:
            sale.save()
        return sale
