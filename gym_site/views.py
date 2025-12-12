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
    return render(request, 'main/about.html')

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
    return render(request, 'main/programs.html', context)

def trainers(request):
    coaches = Coach.objects.all()
    context = {
        'coaches': coaches,
    }
    return render(request, 'main/trainers.html', context)

def schedule(request):
    return render(request, 'main/schedule.html')

def pricing(request):
    return render(request, 'main/pricing.html')

def gallery(request):
    return render(request, 'main/gallery.html')

def contact(request):
    return render(request, 'main/contact.html')
def membership(request):
    """Тарифы и цены (алиас для pricing)"""
    return render(request, 'main/pricing.html')



from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Coach, Program, ContactMessage

def search_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', 'relevance')
    
    results = []
    coaches_count = 0
    programs_count = 0
    
    if query:
        # Поиск по тренерам
        if category in ['all', 'coach']:
            coaches = Coach.objects.filter(
                Q(name__icontains=query) |
                Q(specialization__icontains=query) |
                Q(bio__icontains=query)
            )
            
            for coach in coaches:
                results.append({
                    'type': 'coach',
                    'id': coach.id,
                    'title': coach.name,
                    'specialization': coach.specialization,
                    'description': coach.bio,
                    'photo': coach.photo,
                    'instagram': coach.instagram,
                    'facebook': coach.facebook,
                    'linkedin': coach.linkedin,
                    'url': f'/coaches/{coach.id}/',
                    'model_obj': coach,
                })
                coaches_count += 1
        
        # Поиск по программам
        if category in ['all', 'program']:
            programs = Program.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(coach__name__icontains=query) |
                Q(level__icontains=query) |
                Q(duration__icontains=query)
            )
            
            for program in programs:
                results.append({
                    'type': 'program',
                    'id': program.id,
                    'title': program.title,
                    'description': program.description,
                    'duration': program.duration,
                    'coach': program.coach,
                    'price': program.price,
                    'level': program.level,
                    'get_level_display': program.get_level_display(),
                    'image': program.image,
                    'url': f'/programs/{program.id}/',
                    'model_obj': program,
                })
                programs_count += 1
        
        # Сортировка результатов
        if sort_by == 'name':
            results.sort(key=lambda x: x['title'].lower())
        elif sort_by == 'price_asc':
            results.sort(key=lambda x: float(x.get('price', 0)) if x['type'] == 'program' else float('inf'))
        elif sort_by == 'price_desc':
            results.sort(key=lambda x: float(x.get('price', 0)) if x['type'] == 'program' else float('-inf'), reverse=True)
        else:  # relevance
            # Простой алгоритм релевантности
            results.sort(key=lambda x: (
                query.lower() in x['title'].lower(),
                query.lower() in x.get('specialization', '').lower(),
                query.lower() in x['description'].lower()
            ), reverse=True)
    
    total_count = len(results)
    
    # Пагинация
    paginator = Paginator(results, 12)  # 12 результатов на страницу
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # Популярные запросы
    popular_queries = [
        'персональные тренировки',
        'похудение',
        'набор мышечной массы',
        'йога',
        'кардио',
        'силовые тренировки',
        'фитнес для начинающих',
        'кроссфит',
        'пилатес',
        'стрейчинг'
    ]
    
    # Для русских запросов, добавляем транслитерацию
    suggestions = list(set(popular_queries + [
        'тренер',
        'программа',
        'зал',
        'спорт',
        'здоровье'
    ]))
    
    context = {
        'query': query,
        'category': category,
        'sort': sort_by,
        'results': page_obj.object_list,
        'total_count': total_count,
        'coaches_count': coaches_count,
        'programs_count': programs_count,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'suggestions': suggestions,
    }
    
    return render(request, 'main/search.html', context)


# Детальные views для тренеров и программ
def coach_detail(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    
    # Программы этого тренера
    programs = Program.objects.filter(coach=coach)
    
    context = {
        'coach': coach,
        'programs': programs,
    }
    return render(request, 'main/coach_detail.html', context)

def program_detail(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    
    # Другие программы тренера
    other_programs = Program.objects.filter(coach=program.coach).exclude(id=program_id)[:4]
    
    # Похожие программы по уровню
    similar_programs = Program.objects.filter(
        level=program.level
    ).exclude(id=program_id)[:4]
    
    context = {
        'program': program,
        'other_programs': other_programs,
        'similar_programs': similar_programs,
    }
    return render(request, 'main/program_detail.html', context)


# API для автодополнения
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def search_autocomplete(request):
    query = request.GET.get('q', '').strip()
    
    if query and len(query) >= 2:
        suggestions = []
        
        # Ищем тренеров
        coaches = Coach.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:5]
        
        # Ищем программы
        programs = Program.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True).distinct()[:5]
        
        # Ищем специализации
        specializations = Coach.objects.filter(
            specialization__icontains=query
        ).values_list('specialization', flat=True).distinct()[:5]
        
        # Объединяем и удаляем дубликаты
        all_suggestions = list(coaches) + list(programs) + list(specializations)
        unique_suggestions = []
        seen = set()
        
        for suggestion in all_suggestions:
            if suggestion not in seen:
                seen.add(suggestion)
                unique_suggestions.append(suggestion)
        
        return JsonResponse(unique_suggestions[:10], safe=False)
    
    return JsonResponse([], safe=False)





# Главная страница с поиском
class SearchHomeView(ListView):
    model = Program
    template_name = 'main/search_home.html'
    context_object_name = 'featured_programs'
    paginate_by = 6
    
    def get_queryset(self):
        return Program.objects.all()[:12]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_coaches'] = Coach.objects.all()[:6]
        context['search_query'] = self.request.GET.get('q', '')
        return context