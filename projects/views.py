from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib import messages

from .utils import paginateProjects, searchProjects


# Create your views here.

def projectsPage(request):
    try:
        if request.user.profile:
            profile = request.user.profile
            messages_unread = profile.messages.filter(is_read=False)
            # print(messages_unread)
    except:
        messages_unread = ''

    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = {
        'projects': projects, 
        'search_query': search_query, 
        "custom_range": custom_range,
        "inbox": messages_unread,
        }
    return render(request, "projects/projects.html", context)


def projectPage(request, pk):

    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        profile = request.user.profile
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = profile
            review.project = project
            project.getVote
            review.save()
            return redirect("project", pk=project.id)

    context = {'project': project, "form": form}
    return render(request, "projects/project.html", context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            
            # project_tags = request.POST['tags'].replace(',', " ").split(' ')
            # for tag in project_tags:
            #     if tag:
            #         tag = tag.title()
                    
            # print(project_tags)

            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/projectForm.html", context)



@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    form = ProjectForm(instance=project)
    # print(tags)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            project = form.save(commit=False)
            project_tags = request.POST['tags'].replace(",", " ").split(" ")
            for tag in project_tags:
                tag = tag.title()
                if tag:
                    # Tag.objects.get_or_create(name=tag)
                    project.tags.get_or_create(
                        name=tag
                    )
            project.save()
            return redirect('account')

    context = {'form': form, "project": project}
    return render(request, "projects/projectForm.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        return redirect("account")

    context = {"object": project}
    return render(request, 'projects/delete_template.html', context)
