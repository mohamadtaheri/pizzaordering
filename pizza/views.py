from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza


def home(request):
    return render(request, "pizza/home.html")


def order(request):
    multiple_form = MultiplePizzaForm()

    if request.method == "POST":
        # field_form = PizzaForm(request.POST, request.FILES)
        field_form = PizzaForm(request.POST)

        if field_form.is_valid():                
            current_form = field_form.save()
            current_form_pk = current_form.id
            note = f"Thanks for ordering! Your {field_form.cleaned_data['size']} \
            {field_form.cleaned_data['topping1']} and {field_form.cleaned_data['topping2']} pizza is on its way!"
            field_form = PizzaForm()

        else:
            note = "Your order has been failed! please try again"
            current_form_pk = None
        return render(
            request,
            "pizza/order.html",
            {
                "current_form_pk": current_form_pk,
                "pizzaform": field_form,
                "note": note,
                "multiple_form": multiple_form,
            },
        )

    else:
        form = PizzaForm()
        return render(
            request,
            "pizza/order.html",
            {"pizzaform": form, "multiple_form": multiple_form},
        )


def pizzas(request):
    number_of_pizzas = 2
    field_multiple_pizza = MultiplePizzaForm(request.GET)
    if field_multiple_pizza.is_valid():
        number_of_pizzas = field_multiple_pizza.cleaned_data["number"]

    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == "POST":
        fields_formset = PizzaFormSet(request.POST)
        if fields_formset.is_valid():
            note = "Pizzas have been orders:\n"
            for form in fields_formset:
                form.save()
                note += f"{form.cleaned_data['size']} {form.cleaned_data['topping1']} and {form.cleaned_data['topping2']} \n"
        else:
            note = "Order was not created, please try again!"
        return render(request, "pizza/pizzas.html", {"formset": formset, "note": note})

    else:
        return render(request, "pizza/pizzas.html", {"formset": formset})


def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)

    pizzaform = PizzaForm(instance=pizza)
    if request.method == "POST":
        pizzaform = PizzaForm(request.POST, instance=pizza)
        if pizzaform.is_valid():
            note = "Order has been updated"
            pizzaform.save()
            return render(
                request,
                "pizza/edit_order.html",
                {"pizzaform": pizzaform, "note": note, "pizza": pizza},
            )
    else:
        return render(
            request, "pizza/edit_order.html", {"pizzaform": pizzaform, "pizza": pizza}
        )
