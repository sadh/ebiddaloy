from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.views.generic import UpdateView, CreateView, ListView, TemplateView
from accounts.models import Admin
from django.utils.decorators import method_decorator



# Create your views here.
@method_decorator([login_required, admin_required],name='dispatch')
class AdminDashBoardView(TemplateView):
    model = Admin
    template_name = 'admin_home.html'
