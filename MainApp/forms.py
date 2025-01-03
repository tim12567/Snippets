from django.forms import ModelForm, TextInput, Textarea, ValidationError
from MainApp.models import Comment, Snippet


class SnippetForm(ModelForm):
    class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code', 'public']

       labels = {
          'name': 'Название', 'lang': 'Какой язык', 'code': 'Код', 'public': 'публикация'
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
           

from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput
from django.core.exceptions import ValidationError


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


    password1 = CharField(label="Создайте пароль", widget=PasswordInput)
    password2 = CharField(label="Введите пароль повторно", widget=PasswordInput)

    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['data-custom'] = 'value'


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 3:
           return username
        raise ValidationError('Слишком короткое имя username')

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user          


class CommentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ['text']
       labels = {'text': ''} 
       widgets = {
           'text': Textarea(attrs={'placeholder': 'Комментарий для сниппета'})
       }