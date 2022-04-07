from .models import Skill, Profile
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginateProfiles(request, profiles, results):
    
    page = request.GET.get('page')

    pagin = Paginator(profiles, results)
    try:
        profiles = pagin.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = pagin.page(page)
    except EmptyPage:
        page = pagin.num_pages
        profiles = pagin.page(page)
        messages.error(request, "You reached last page!")

    leftIndex = (int(page)-1)
    rightIndex = (int(page) + 2)

    if leftIndex < 1:
        leftIndex = 1
        rightIndex = (int(page) + 3)
    
    if rightIndex > pagin.num_pages:
        rightIndex = pagin.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles



def searchProfile(request):
    
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_info__icontains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query