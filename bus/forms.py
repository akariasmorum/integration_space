from django import forms

class Start_script_form(forms.Form):
	name = forms.CharField(label='Название скрипта', widget = forms.TextInput(attrs={'class': 'form-control','id':'script_name', }), max_length=14)
	priority = forms.CharField(label='Приоритет скрипта', widget = forms.TextInput(attrs={'class': 'form-control' , 'id': 'script_priority' }))
	params = forms.CharField(label='Параметры скрипта', widget = forms.TextInput(attrs={'class': 'form-control' , 'id': 'script_params'}))
	