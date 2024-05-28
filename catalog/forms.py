from django import forms

from catalog.models import Comments, Product, Version
from common.views import StyleFormMixin


class CommentsForm(forms.ModelForm):
    """
    Класс для работы с формой "CommentsForm"
    """
    class Meta:
        model = Comments
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }


class ProductCreateForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для работы с формой "ProductCreateForm"
    """
    class Meta:
        model = Product
        fields = ('name', 'description', 'avatar', 'category', 'price', 'quantity')

    def clean_name(self):
        """
        Проверка на наличие запрещенных слов в названии товара
        """
        cleaned_data = self.cleaned_data.get('name')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Недопустимы слова в названии')

        return cleaned_data

    def clean_description(self):
        """
        Проверка на наличие запрещенных слов в описании товара
        """
        cleaned_data = self.cleaned_data.get('description')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Недопустимы слова в описании')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для работы с формой "VersionForm"
    """
    class Meta:
        model = Version
        fields = ('number_version', 'version_name', 'version_flag')


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для работы с формой "ProductCreateForm"
    """
    class Meta:
        model = Product
        fields = ('description', 'category', 'publication_sign')
