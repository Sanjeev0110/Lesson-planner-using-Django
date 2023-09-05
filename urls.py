"""NotesSharingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notes.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',AboutView.as_view(),name='about'),
    path('',IndexView.as_view(),name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login_admin/', LoginAdminView.as_view(), name='login_admin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('admin_home/', AdminHomeView.as_view(), name='admin_home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('review/', reviewquestionsView1.as_view(), name='review'),

    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('upload_notes/', UploadNotesView.as_view(), name='upload_notes'),
    path('reviewquestions/', reviewquestionsView.as_view(), name='reviewquestions'),
    path('delete_mynotes/<int:pid>', DeleteMyNotesView.as_view(), name='delete_mynotes'),
    path('view_allnotes/', ViewAllNotesView.as_view(), name='view_allnotes'),
    path('view_users/', ViewUsersView.as_view(), name='view_users'),
    path('delete_users/<int:pid>', DeleteUsersView.as_view(), name='delete_users'),
    path('pending_notes/', PendingNotesView.as_view(), name='pending_notes'),
    path('accepted_notes/', AcceptedNotesView.as_view(), name='accepted_notes'),
    path('rejected_notes/', RejectedNotesView.as_view(), name='rejected_notes'),
    path('all_notes/', AllNotesView.as_view(), name='all_notes'),
    path('assign_status/<int:pid>', AssignStatusView.as_view(), name='assign_status'),
    path('delete_notes/<int:pid>', DeleteNotesView.as_view(), name='delete_notes'),
    path('viewallnotes/', ViewAllNotesView.as_view(), name='viewallnotes'),
    path('change_passwordadmin/', ChangePasswordAdminView.as_view(), name='change_passwordadmin'),
    path('unread_queries', UnreadQueriesView.as_view(), name='unread_queries'),
    path('read_queries', ReadQueriesView.as_view(), name='read_queries'),
    path('view_queries/<int:pid>', ViewQueriesView.as_view(), name='view_queries'),
    path('course_details/', Course_detailsView.as_view(), name='course_details'),
    path('Upload_Course_Details/', Upload_Course_DetailsView.as_view(), name='Upload_Course_Details'),
    path('assignment/', UploadAssignmentView.as_view(), name='assignment'),
    path('view_assignment/', SubmitassignmentView.as_view(), name='view_assignment'),
    path('Upload_assignment/', Upload_assignment_View.as_view(), name='Upload_assignment'),
    path('Course_admin/', Course_detailsadmin.as_view(), name='Course_admin'),
    path('delete/<int:pid>', delete, name='delete'),
    path('delete_course/<int:pid>', delete_course, name='delete_course'),
    path('create_question/', CreateQuestionView.as_view(), name='create_question'),
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
