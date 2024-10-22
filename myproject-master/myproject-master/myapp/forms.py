from django import forms
from .models import Threshold


class ThresholdForm(forms.ModelForm):
    class Meta:
        model = Threshold
        fields = ['employee', 'questionnaire', 'min_value',
                  'max_value', 'exact_value', 'threshold_type']
        widgets = {
            'threshold_type': forms.Select(choices=Threshold.THRESHOLD_TYPE_CHOICES),
        }
