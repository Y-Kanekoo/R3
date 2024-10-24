from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.admin.views.decorators import staff_member_required
from .forms.signup import SignUpForm

from django.contrib.auth import get_user_model


def profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST["email"]
        user.username = request.POST["username"]
        user.save()
        return redirect("profile")
    else:
        return render(request, "accounts/profile.html")




class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("profile")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())

User = get_user_model()
@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@staff_member_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return redirect('accounts/user_list')

    return render(request, 'accounts/user_list.html')