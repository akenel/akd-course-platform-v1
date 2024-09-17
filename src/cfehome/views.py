from django.conf import settings
from django.shortcuts import render

from emails.forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS
def home_view(request, *args, **kwargs):
    template_name = "home.html"
    # request POST data
    print(request.POST)
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": ""
    }
    if form.is_valid():
        obj = form.save()
        print(obj)
        context['form'] = EmailForm()
        context['message'] = f"Succcess! Check your email for verification from {EMAIL_ADDRESS}"
    else:
        print(form.errors) 
    return render(request, template_name, context)