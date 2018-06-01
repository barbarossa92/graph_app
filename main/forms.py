from django import forms
from django.core.validators import FileExtensionValidator
import xml.etree.cElementTree as etree
from django.conf import settings as st


class GraphImport(forms.Form):

    graph_file = forms.FileField(label="Импортировать граф", validators=[FileExtensionValidator(allowed_extensions=['xml'])])

    def __init__(self, *args, **kwargs):
        super(GraphImport, self).__init__(*args, **kwargs)
        for f in self.visible_fields():
            f.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        data = super().clean()
        graph_file = data.get("graph_file")
        if graph_file:
            try:
                tree = etree.fromstring(graph_file.read())
            except etree.ParseError:
                raise forms.ValidationError("Проверьте правильность содержимого файла")
            nodes = list()
            groups = list()
            for element in tree.iter():
                if element.tag == "node":
                    nodes.append({"eid": element.get("eid"), "text": element.text})
                elif element.tag == "group":
                    groups.append({"eid": element.get("eid"), "text": element.text,
                                   "groupped": element.get("groupped", "")})
                else:
                    pass

            """Проверка на коллизию значений атрибута 'eid'"""
            uniq_eids = [i["eid"] for i in nodes + groups if i["eid"]]
            if len(uniq_eids) > len(set(uniq_eids)):
                raise forms.ValidationError("Атрибут 'eid' должен быть уникальным")

            """Проверка на содержание группы не менее двух существуюших элементов"""
            msg = "Атрибут 'groupped' должен содержать не менее %s существуюших 'eid'" % st.GROUP_MIN_ELEMENTS
            for i in groups:
                if len(i["groupped"].split()) < st.GROUP_MIN_ELEMENTS:
                    raise forms.ValidationError(msg)
                for j in i["groupped"].split():
                    if j not in uniq_eids:
                        raise forms.ValidationError(msg)

            data["nodes"] = nodes
            data["groups"] = groups
        return data