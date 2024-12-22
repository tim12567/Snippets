from django.forms import ModelForm, TextInput, Textarea, ValidationError
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code']

       labels = {
          'name': 'Название', 'lang': 'Какой язык', 'code': 'Код'
      }
       widgets = {
                    'name': TextInput(attrs={'placeholder': 'Название сниппета'}),
                    'code': Textarea(attrs={'placeholder': 'Код текста'}),
                  }
       

    def clean_name(self):
       snippet_name = self.cleaned_data.get('name')
       if len(snippet_name) > 3:
           return snippet_name
       raise ValidationError('Слишком короткое имя сниппета')
           