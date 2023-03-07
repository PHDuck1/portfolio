from django import forms


class FileFieldForm(forms.Form):
    name = forms.CharField(max_length=30)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    image_previews = forms.CharField(widget=forms.HiddenInput(), required=False)
