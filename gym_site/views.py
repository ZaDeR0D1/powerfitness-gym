from django.shortcuts import render
from .models import Coach, Program

def index(request):
    coaches = Coach.objects.all()[:4]
    programs = Program.objects.all()[:3]
    
    context = {
        'coaches': coaches,
        'programs': programs,
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/pages/about.html')

def programs_page(request):
    programs = Program.objects.all()
    levels = Program.LEVEL_CHOICES
    
    level_filter = request.GET.get('level')
    if level_filter:
        programs = programs.filter(level=level_filter)
    
    context = {
        'programs': programs,
        'levels': levels,
        'selected_level': level_filter,
    }
    return render(request, 'main/pages/programs.html', context)

def trainers(request):
    coaches = Coach.objects.all()
    context = {
        'coaches': coaches,
    }
    return render(request, 'main/pages/trainers.html', context)

def schedule(request):
    return render(request, 'main/pages/schedule.html')

def pricing(request):
    return render(request, 'main/pages/pricing.html')

def gallery(request):
    return render(request, 'main/pages/gallery.html')

def contact(request):
    return render(request, 'main/pages/contact.html')
def membership(request):
    """Тарифы и цены (алиас для pricing)"""
    return render(request, 'main/pages/pricing.html')