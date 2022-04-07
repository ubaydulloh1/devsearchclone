from django.urls import path
from . import views


urlpatterns = [
    path("user-login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerUser, name="register"),

    path("account/", views.userAccount, name="account"),
    path("edit-account", views.editAccount, name="edit-account"),

    path("", views.profilesPage, name="home"),
    path("user-profile/<str:pk>/", views.userProfile, name="user-profile"),

    path("add-skill", views.addSkill, name="add-skill" ),
    path("update-skill/<str:pk>", views.updateSkill, name="update-skill" ),
    path("delete-skill/<str:pk>", views.deleteSkill, name="delete-skill" ),

    path("inbox/", views.messagesInbox, name="inbox"),
    path("message/<str:pk>/", views.messageInbox, name="message"),
    path("create-message/<str:pk>/", views.createMessage, name="create-message"),
]

