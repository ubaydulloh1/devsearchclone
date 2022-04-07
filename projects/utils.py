from .models import Project, Tag
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginateProjects(request, projects, results):
    
    page = request.GET.get('page')

    pagin = Paginator(projects, results)
    try:
        projects = pagin.page(page)
    except PageNotAnInteger:
        page = 1
        projects = pagin.page(page)
    except EmptyPage:
        page = pagin.num_pages
        projects = pagin.page(page)
        messages.error(request, "You reached last page!")

    leftIndex = (int(page)-1)
    rightIndex = (int(page) + 2)

    if leftIndex < 1:
        leftIndex = 1
        rightIndex = (int(page) + 3)
    
    if rightIndex > pagin.num_pages:
        rightIndex = pagin.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects



def searchProjects(request):
    
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects, search_query