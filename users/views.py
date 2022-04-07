from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UpdateUserProfileForm, SkillForm, MessageForm
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth.models import User
from .models import Profile
from .utils import searchProfile, paginateProfiles


# Create your views here.

def loginPage(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username not found!")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        else:
            messages.error(request, "username or password is incorrect")

    context = {}
    return render(request, "users/login_register.html", context)


def logoutPage(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("home")



def registerUser(request):
    form = CustomUserCreationForm()


    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, f"Successfully {user.username} Registered!")

            return redirect("edit-account")
        else:
            messages.error(request, "Something went wrong!")
            return redirect("register")


    context = {"page": "register", 'form': form}

    return render(request, "users/login_register.html", context)




def profilesPage(request):
    try:
        if request.user.profile:
            profile = request.user.profile
            messages_unread = profile.messages.filter(is_read=False)
            # print(messages_unread)
    except:
        messages_unread = ''

    profiles, search_query = searchProfile(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)
    
    context = {"profiles": profiles, 'search_query': search_query, "custom_range": custom_range, "inbox": messages_unread}
    return render(request, "users/profiles.html", context)


def userProfile(request, pk):

    try:
        if request.user.profile:
            profile = request.user.profile
            messages_unread = profile.messages.filter(is_read=False)
            # print(messages_unread)
    except:
        messages_unread = ''

    user_profile = Profile.objects.get(id=pk)

    primary_skills = user_profile.skill_set.exclude(description="")
    other_skills = user_profile.skill_set.filter(description="")

    context = {
        'profile': user_profile, 
        "topSkills": primary_skills, 
        "otherSkills": other_skills,
        "inbox": messages_unread
        }
    return render(request, "users/user_profile.html", context)



def userAccount(request):
    profile = request.user.profile
    try:
        if request.user.profile:
            profile = request.user.profile
            messages_unread = profile.messages.filter(is_read=False)
            # print(messages_unread)
    except:
        messages_unread = ''

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        "profile": profile, 
        "skills": skills, 
        "projects": projects,
        "inbox": messages_unread,
        }
    return render(request, "users/user_account.html", context)



@login_required(login_url="login")
def editAccount(request):

    profile = request.user.profile

    form = UpdateUserProfileForm(instance=profile)

    if request.method == "POST":
        form = UpdateUserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {"form": form}
    return render(request, "users/user_update.html", context)


@login_required(login_url="login")
def addSkill(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect("account")
    else:
        form = SkillForm()
        context = {"form": form}

    return render(request, "users/skills_form.html", context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skills_form.html", context)



@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        return redirect("account")

    context = {"object": skill}
    return render(request, 'projects/delete_template.html', context)


@login_required(login_url="login")
def messagesInbox(request):

    messages_user = request.user.profile.messages.all()
    messages_is_read = request.user.profile.messages.filter(is_read=False)

    context = {"messages_": messages_user, "messages_is_read": messages_is_read}
    return render(request, "users/inbox.html", context)


def messageInbox(request, pk):
    message_single = request.user.profile.messages.get(id=pk)
    
    if message_single.is_read == False:
        message_single.is_read = True
        message_single.save()
    
    context = {"message_single": message_single}
    return render(request, "users/message.html", context)


def createMessage(request, pk):

    form = MessageForm()

    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
    except:
        sender = None


    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.reciever = recipient
            message.sender = sender

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect("user-profile", pk=recipient.id)


    context = {"reciepent": recipient, "form": form}
    return render(request, "users/message_form.html", context)