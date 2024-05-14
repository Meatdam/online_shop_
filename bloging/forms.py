from django import forms

from bloging.models import Blog


class AddBlogForm(forms.ModelForm):
    """
    Класс для работы с формой "AddPostForm"
    """
    class Meta:
        model = Blog
        fields = ('title', 'description', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'btn'}),
            }

