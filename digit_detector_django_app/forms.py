from django import forms

class CanvasForm(forms.Form):
    canvas_form = forms.CharField(label='Canvas')
