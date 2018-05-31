from django import forms
from django.core.validators import FileExtensionValidator


class GraphImport(forms.Form):

    graph_file = forms.FileField(label="Создать граф", validators=[FileExtensionValidator(allowed_extensions=['xml'])])