from django.shortcuts import render

def about(request, template_name="about.html"):
    return render(request, template_name)