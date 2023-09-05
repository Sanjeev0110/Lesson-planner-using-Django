from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from datetime import date
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
# Create your views here.

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', {})

    def post(self, request):
        error = ""
        if request.method == 'POST':
            f = request.POST.get('fullname')
            em = request.POST.get('email')
            m = request.POST.get('mobile')
            s = request.POST.get('subject')
            msg = request.POST.get('message')
            try:
                Contact.objects.create(fullname=f, email=em, mobile=m, subject=s, message=msg, msgdate=date.today(), isread="no")
                error = "no"
            except:
                error = "yes"

        return render(request, 'contact.html', {'error': error})

class UserLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        error = ""
        return render(request, self.template_name, {'error': error})

    def post(self, request):
        error = ""
        u = request.POST.get('emailid')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)

        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
        return render(request, self.template_name, {'error': error})


class LoginAdminView(View):
    template_name = 'login_admin.html'

    def get(self, request):
        return render(request, self.template_name, {'error': ''})

    def post(self, request):
        error = ""
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect( 'admin_home')
        else:
            error = "yes"

        return render(request, self.template_name, {'error': error})


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = SignupForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        f = request.POST.get('firstname')
        l = request.POST.get('lastname')
        c = request.POST.get('contact')
        e = request.POST.get('emailid')
        p = request.POST.get('password')
        pas=make_password(p)
        users = User.objects.create(username=e, password=pas, first_name=f, last_name=l)

        form = SignupForm(request.POST)
        if form.is_valid():
            post_form=form.save(commit=False)

            post_form.user=users
            post_form.save()
            return HttpResponseRedirect('/login')
        context = {'form': form}
        return render(request,'login', context)

        return HttpResponseRedirect('login',{'error': error})

class AdminHomeView(View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('login_admin')

        pn = Notes.objects.filter(status="pending").count()
        an = Notes.objects.filter(status="Accept").count()
        rn = Notes.objects.filter(status="Reject").count()
        alln = Notes.objects.all().count()

        d = {'pn': pn, 'an': an, 'rn': rn, 'alln': alln}
        return render(request, 'admin_home.html', d)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        # print(user)
        if user.is_superuser:
            data = User.objects.get(username=user)

            d = {'data': data}
            return render(request, 'profile.html', {'data':data})
        else:
            data = Signup.objects.get(user_id=user)

            d = {'data': data, 'user': user}
            return render(request, 'profile.html', d)


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = Signup.objects.get(user=user)
        error = False

        d = {'data': data, 'user': user, 'error': error}
        return render(request, 'edit_profile.html', d)

    def post(self, request):
        user = request.user
        data = Signup.objects.get(user=user)
        error = False
        if request.method == 'POST':
            f = request.POST['firstname']
            l = request.POST['lastname']
            c = request.POST['contact']
            b = request.POST['branch']
            user.first_name = f
            user.last_name = l
            data.contact = c
            data.branch = b
            user.save()
            data.save()
            error = True

        d = {'data': data, 'user': user, 'error': error}
        return render(request, 'edit_profile.html', d)

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        error = ""
        return render(request, 'changepassword.html', {'error': error})

    def post(self, request):
        error = ""
        if request.method == 'POST':
            o = request.POST['old']
            n = request.POST['new']
            c = request.POST['confirm']
            if c == n:
                u = User.objects.get(username__exact=request.user.username)
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "yes"

        return render(request, 'changepassword.html', {'error': error})

class UploadNotesView(LoginRequiredMixin, View):
    def get(self, request):
        error = ""
        return render(request, 'upload_notes.html', {'error': error})

    def post(self, request):
        error = ""
        if request.method == 'POST':
            b = request.POST['branch']
            s = request.POST['subject']
            n = request.FILES['notesfile']
            f = request.POST['filetype']
            d = request.POST['description']
            u = User.objects.filter(username=request.user.username).first()
            try:
                Notes.objects.create(user=u, uploadingdate=date.today(), branch=b, subject=s, notesfile=n,
                                     filetype=f, description=d, status='pending')
                error = "no"
            except:
                error = "yes"

        return render(request, 'upload_notes.html', {'error': error})

# class ViewMyNotesView(LoginRequiredMixin, View):
#     def get(self, request):
#         user = request.user
#         Reviewquestions = reviewquestions.objects.get()
#
#         d = {'notes': notes}
#         return render(request, 'reviewquestions.html', d)

class DeleteMyNotesView(LoginRequiredMixin, View):
    def post(self, request, pid):
        notes = Notes.objects.get(id=pid)
        notes.delete()
        return redirect('view_mynotes')

class ViewAllNotesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        notes = Notes.objects.filter(user=user)

        d = {'notes': notes}
        return render(request, 'view_allnotes.html', d)

class ViewUsersView(LoginRequiredMixin, View):
    def get(self, request):
        users = Signup.objects.all()

        d = {'users': users}
        return render(request, 'view_users.html', d)

class DeleteUsersView(LoginRequiredMixin, View):
    def post(self, request, pid):
        user = User.objects.get(id=pid)
        user.delete()
        return redirect('view_users')

class PendingNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = Notes.objects.filter(status="pending")
        d = {'notes': notes}
        return render(request, 'pending_notes.html', d)

class AcceptedNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = Notes.objects.filter(status="Accept")
        d = {'notes': notes}
        return render(request, 'accepted_notes.html', d)

class RejectedNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = Notes.objects.filter(status="Reject")
        d = {'notes': notes}
        return render(request, 'rejected_notes.html', d)

class AllNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = Notes.objects.all()
        d = {'notes': notes}
        return render(request, 'all_notes.html', d)

class AssignStatusView(LoginRequiredMixin, View):
    def get(self, request, pid):
        notes = Notes.objects.get(id=pid)
        error = ""
        d = {'notes': notes, 'error': error}
        return render(request, 'assign_status.html', d)

    def post(self, request, pid):
        notes = Notes.objects.get(id=pid)
        error = ""
        if request.method == 'POST':
            s = request.POST['status']
            try:
                notes.status = s
                notes.save()
                error = "no"
            except:
                error = "yes"

        d = {'notes': notes, 'error': error}
        return render(request, 'assign_status.html', d)

class DeleteNotesView(LoginRequiredMixin, View):
    def post(self, request, pid):
        notes = Notes.objects.get(id=pid)
        notes.delete()
        return redirect('all_notes')

class ViewAllNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = Notes.objects.filter(status='Accept')
        d = {'notes': notes}
        return render(request, 'viewallnotes.html', d)

class ChangePasswordAdminView(LoginRequiredMixin, View):
    def get(self, request):
        error = ""
        return render(request, 'change_passwordadmin.html', {'error': error})

    def post(self, request):
        error = ""
        user = request.user
        if request.method == "POST":
            o = request.POST['oldpassword']
            n = request.POST['newpassword']
            c = request.POST['confirmpassword']
            try:
                if user.check_password(o):
                    user.set_password(n)
                    user.save()
                    error = "no"
                else:
                    error = 'not'
            except:
                error = "yes"
        return render(request, 'change_passwordadmin.html', {'error': error})

class UnreadQueriesView(LoginRequiredMixin, View):
    def get(self, request):
        contact = Contact.objects.filter(isread="no")
        return render(request, 'unread_queries.html', {'contact': contact})

class ReadQueriesView(LoginRequiredMixin, View):
    def get(self, request):
        contact = Contact.objects.filter(isread="yes")
        return render(request, 'read_queries.html', {'contact': contact})

class ViewQueriesView(LoginRequiredMixin, View):
    def get(self, request, pid):
        contact = Contact.objects.get(id=pid)
        contact.isread = "yes"
        contact.save()
        return render(request, 'view_queries.html', {'contact': contact})




# class Course_detailsView(LoginRequiredMixin, View):
#     def get(self, request):
#         error = ""
#         return render(request, 'course_details.html', {'error': error})
#
#     def post(self, request):
#         error = ""
#         if request.method == 'POST':
#             b = request.POST['Course_code']
#             s = request.POST['Course_Title']
#             n = request.FILES['L_T_P']
#             f = request.POST['Credits']
#             d = request.POST['Contact_Hrs']
#             i = request.POST['ISA_Marks']
#             e = request.POST['ESA_Marks']
#             t = request.POST['Total_Marks']
#             x = request.POST['Exam_Duration']
#
#
#             u = User.objects.filter(username=request.user.username).first()
#             try:
#                 Notes.objects.create(user=u, uploadingdate=date.today(), branch=b, subject=s, notesfile=n,
#                                      filetype=f, description=d, status='pending')
#                 error = "no"
#             except:
#                 error = "yes"
#
#         return render(request, 'course_details.html', {'error': error})
#

class Upload_Course_DetailsView(LoginRequiredMixin, View):
    def get(self, request):
        error = ""
        return render(request, 'Upload_Course_Details.html', {'error': error})

    def post(self, request):
        error = ""
        if request.method == 'POST':
            b = request.POST['branch']
            s = request.POST['subject']
            n = request.FILES['notesfile']
            f = request.POST['filetype']
            d = request.POST['description']
            u = User.objects.filter(username=request.user.username).first()
            try:
                Course.objects.create(user=u, uploadingdate=date.today(), branch=b, subject=s, notesfile=n,
                                     filetype=f, description=d, status='pending')
                error = "no"
            except:
                error = "yes"

        # Redirect to a valid URL name, using the 'reverse' function
        if error == "no":
            return redirect('Course_admin')  # Replace 'Course_Details' with the correct URL name
        else:
            return render(request, 'Upload_Course_Details.html', {'error': error})



# class Course_detailsView(LoginRequiredMixin, View):
#     def get(self, request):
#         error = ""
#         return render(request, 'course_details.html', {'error': error})
#
#     def post(self, request):
#         error = ""
#         if request.method == 'POST':
#             b = request.POST['Course_code']
#             s = request.POST['Course_Title']
#             n = request.FILES['L_T_P']
#             f = request.POST['Credits']
#             d = request.POST['Contact_Hrs']
#             i = request.POST['ISA_Marks']
#             e = request.POST['ESA_Marks']
#             t = request.POST['Total_Marks']
#             x = request.POST['Exam_Duration']
#
#
#             u = User.objects.filter(username=request.user.username).first()
#             try:
#                 Course.objects.create(user=u, uploadingdate=date.today(), branch=b, subject=s, notesfile=n,
#                                      filetype=f, description=d, status='pending')
#                 error = "no"
#             except:
#                 error = "yes"
#
#         return render(request, 'course_details.html', {'error': error})
#
# class Course_detailsView(LoginRequiredMixin, View):
#     def get(self, request):
#         course = Course.objects.filter(status="Reject")
#         d = {'course': course}
#         return render(request, 'course_details.html', d)
#display View

class Course_detailsView(LoginRequiredMixin, View):
    def get(self, request):
        disp=Course.objects.all()
        return render(request,'course_details.html',{'disp':disp})

class Course_detailsadmin(LoginRequiredMixin, View):
    def get(self, request):
        disp=Course.objects.all()
        return render(request,'admin_course.html',{'disp':disp})

class UploadAssignmentView(View):
    template_name = 'assignment.html'

    def get(self, request):
        form = AssignmentForm()  # Initialize an empty form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AssignmentForm(request.POST, request.FILES)  # Populate form with POST data

        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('view_assignment')  # Redirect to a success page

        return render(request, self.template_name, {'form': form})
class SubmitassignmentView(View):
    template_name = 'view_assignment.html'

    def get(self, request):
        assignment = Assignment.objects.get()
        return render(request, self.template_name, {'assignment': assignment})


class Upload_assignment_View(LoginRequiredMixin, View):
    def get(self, request):
        error = ""
        return render(request, 'Upload_Course_Details.html', {'error': error})

    def post(self, request):
        error = ""
        if request.method == 'POST':
            b = request.POST['branch']
            s = request.POST['subject']
            n = request.FILES['notesfile']
            f = request.POST['filetype']
            d = request.POST['description']
            u = User.objects.filter(username=request.user.username).first()
            try:
                Course.objects.create(user=u, uploadingdate=date.today(), branch=b, subject=s, notesfile=n,
                                     filetype=f, description=d, status='pending')
                error = "no"
            except:
                error = "yes"

        return render(request, 'course_details.html', {'error': error})

class reviewquestionsView(View):
    template_name = 'reviewquestions.html'

    def get(self, request):
        reviews = Reviewque.objects.filter(user=request.user)
        return render(request, self.template_name, {'reviews': reviews})

class reviewquestionsView1(View):
    template_name = 'user_review_user.html'

    def get(self, request):
        reviews = Reviewque.objects.all()
        return render(request, self.template_name, {'reviews': reviews})


class UploadNotesView(View):
    template_name = 'upload_notes.html'
    form_class = ReviewqueForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():

            user = User.objects.get(username=request.user.username)  # Assuming user is authenticated
            review = form.save(commit=False)
            review.user = user
            review.save()
            return redirect('reviewquestions')
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})



# class DeleteReviewquestionsView(LoginRequiredMixin, View):
def delete(request,pid):
    reviews = Reviewque.objects.get(id=pid)
    reviews.delete()
    return redirect('reviewquestions')

def delete_course(request,pid):
    disp = Course.objects.get(id=pid)
    disp.delete()
    return redirect('Course_admin')


class CreateQuestionView(View):
    template_name = 'question_form.html'

    def get(self, request, *args, **kwargs):
        question_form = QuestionForm()
        answer_form = AnswerForm()
        return render(request, self.template_name, {'question_form': question_form, 'answer_form': answer_form})

    def post(self, request, *args, **kwargs):
        question_form = QuestionForm(request.POST)
        answer_form = AnswerForm(request.POST)

        if question_form.is_valid() and answer_form.is_valid():
            question = question_form.save()
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('quiz_list')

        return render(request, self.template_name, {'question_form': question_form, 'answer_form': answer_form})




