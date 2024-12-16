from django import forms
from .models import Pizza
from django.core.exceptions import ValidationError

# class PizzaForm(forms.Form):
#     # toppings = forms.ChoiceField(choices=[('pep','Peperoni'),('cheese','Cheese'),('olive','Olive')], widget=forms.CheckboxSelectMultiple)
#     topping1 = forms.CharField(label='Topping 1:', max_length=100)
#     topping2 = forms.CharField(label='Topping 2:', max_length=100)
#     size = forms.ChoiceField(label='Size:', choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    

class MultiplePizzaForm(forms.Form):
    number = forms.IntegerField(min_value=2, max_value=6)

class PizzaForm(forms.ModelForm):
    
    # size = forms.ModelChoiceField(queryset=Size.objects.all(),empty_label='Select ...')
    # image = forms.ImageField()
    class Meta:
        model = Pizza
        fields = '__all__'        
        labls = {
            'topping1' : 'Topping1 ',
        }
    
    def clean_topping1(self):
        data = self.cleaned_data["topping1"]
        if 'sample' in data:
            raise ValidationError('We donot accept "sample" topping ')
        return data
   
        