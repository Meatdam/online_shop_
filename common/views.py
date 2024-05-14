class TitleMixin:
    """
    Миксин для добавления заголовка в контекст
    """
    title = None

    def get_context_data(self, **kwargs):
        """
        Добавление заголовка в контекст
        :param kwargs:
        :return:
        """
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class StyleFormMixin:
    """
    Миксин для добавления стилей в формы
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
