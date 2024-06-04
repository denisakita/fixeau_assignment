from django import forms

class GroundLevelForm(forms.Form):
    ground_level = forms.FloatField(label='Ground Level')
