from django import forms
from .models import DataFile,Nlutext
import magic
from django.core.exceptions import ValidationError

class DataFileForm(forms.ModelForm):
    def clean_data(self):
        file = self.cleaned_data.get("data", False)
        if file:
            filetype = magic.from_buffer(file.read())
            if not "csv" in file.name:
                raise ValidationError("File is not CSV.")
            return file

    class Meta:
        model = DataFile
        fields = ('data',)
        # exclude = ('filename',)

class NlutextForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Nlutext
        exclude = ('created_at', 'trained_at')
# class MyArticleAdminForm(forms.ModelForm):
#     def clean_name(self):
#         # do something that validates your data
#         return self.cleaned_data["name"]