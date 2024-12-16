from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory

def home(request):
    return render(request, 'pizza/home.html')


def order(request):
    multiple_form = MultiplePizzaForm()
    
    if request.method == 'POST':
        # field_form = PizzaForm(request.POST, request.FILES)
        field_form = PizzaForm(request.POST)
        field_form.save()
        if field_form.is_valid():
            note = f'Thanks for ordering! Your {field_form.cleaned_data['size']} \
            {field_form.cleaned_data['topping1']} and {field_form.cleaned_data['topping2']} pizza is on its way!'
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'pizzaform': new_form, 'note': note, 'multiple_form': multiple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form': multiple_form})
    

def pizzas(request):
    number_of_pizzas = 2 
    field_multiple_pizza = MultiplePizzaForm(request.GET)
    if field_multiple_pizza.is_valid():
        number_of_pizzas = field_multiple_pizza.cleaned_data['number']
    
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        fields_formset = PizzaFormSet(request.POST)
        if fields_formset.is_valid():
            note = 'Pizzas have been orders:\n'
            for form in fields_formset:
                note += f'{form.cleaned_data['size']} {form.cleaned_data['topping1']} and {form.cleaned_data['topping2']} \n'
        else:
            note = 'Order was not created, please try again!'
        return render(request, 'pizza/pizzas.html', {'formset': formset, 'note': note})
            
    else:
         return render(request, 'pizza/pizzas.html', {'formset': formset})
