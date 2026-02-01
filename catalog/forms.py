from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем Bootstrap-классы ко всем полям
        for field_name, field in self.fields.items():
            widget = field.widget

            # Основной класс для всех полей
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'

            # Особый стиль для чекбоксов (если бы были) — не требуется здесь
            # Для FileField (изображение) можно оставить как есть или уточнить
            if isinstance(widget, forms.FileInput):
                widget.attrs['class'] = 'form-control-file'

        # Дополнительно: placeholder и шаг для цены
        self.fields['name'].widget.attrs.update({'placeholder': 'Введите название товара'})
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Описание товара',
            'rows': 4
        })
        self.fields['price'].widget.attrs.update({
            'placeholder': '0.00',
            'step': '0.01'
        })

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        self._check_forbidden_words(name, 'name')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        self._check_forbidden_words(description, 'description')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def _check_forbidden_words(self, text, field_name):
        if not text:
            return
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in text_lower:
                raise forms.ValidationError(
                    f"Слово '{word}' запрещено к использованию в поле '{field_name}'."
                )
