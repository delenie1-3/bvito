from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import AdvUser
from .forms import ChangeUserInfoForm, RegisterUserForm

from django.contrib.auth.views import PasswordChangeView

from django.core.signing import BadSignature
from .utilities import signer

from django.contrib.auth import logout
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q

from .models import SubRubric, Bv
from .forms import SearchForm, BvForm, AIFormSet
from django.shortcuts import redirect

from .models import Comment
from .forms import UserCommentForm, GuestCommentForm


def index(request):#контроллер-функция главной страницы
    bbs = Bv.objects.filter(is_active=True)[:10]
    context = {'bbs':bbs}
    return render(request, 'main/index.html', context)

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class BVLoginView(LoginView):
    template_name = 'main/login.html'

class BVLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):#контроллер смены данных пользователя
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class BVPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):#Контроллер смены пароля
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя иземнён'

@login_required
def profile(request):#страница пользователя
    return render(request, 'main/profile.html')

class RegisterUserView(CreateView):#контроллер регистрации пользователя
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):#успешная регистрация
    template_name = 'main/register_done.html'

def user_activate(request, sign):#активация пользователя
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):#контроллер класса удаления пользователя
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self,queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

def by_rubric(request,pk):#список объявлений
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bv.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword':keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric':rubric, 'page':page, 'bbs':page.object_list, 'form':form}
    return render(request, 'main/by_rubric.html', context)

def detail(request, rubric_pk, pk):#контроллер сведений
    bv = Bv.objects.get(pk=pk)
    ais = bv.additionalimage_set.all()
    comments = Comment.objects.filter(bv=pk, is_active=True)
    initial = {'bv':bv.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {'bv':bv, 'ais':ais, 'comments':comments, 'form':form}
    return render(request, 'main/detail.html', context)
    #детали объявления без капчи
    '''bv = get_object_or_404(Bv, pk=pk)
    ais = bv.additionalimage_set.all()
    context = {'bv':bv, 'ais':ais}
    return render(request, 'main/detail.html', context)'''   

@login_required
def profile(request):
    bbs = Bv.objects.filter(author=request.user.pk)
    context = {'bbs':bbs}
    return render(request, 'main/profile.html', context)

@login_required
def profile_bv_detail(request, pk):#контроллер сведений конкретного пользователя
    bv = Bv.objects.get(pk=pk)
    ais = bv.additionalimage_set.all()
    comments = Comment.objects.filter(bv=pk, is_active=True)
    initial = {'bv':bv.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {'bv':bv, 'ais':ais, 'comments':comments, 'form':form}
    return render(request, 'main/profile_bv_detail.html', context) 

@login_required
def profile_bv_add(request):
    if request.method == 'POST':
        form = BvForm(request.POST, request.FILES)
        if form.is_valid():
            bv = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bv)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
                return redirect('main:profile')
    else:
        form = BvForm(initial={'author':request.user.pk})
        formset = AIFormSet()
    context = {'form':form,'formset':formset}
    return render(request, 'main/profile_bv_add.html', context)

@login_required
def profile_bv_change(request, pk):
    bv = get_object_or_404(Bv, pk=pk)
    if request.method == 'POST':
        form = BvForm(request.POST, request.FILES, instance=bv)
        if form.is_valid():
            bv = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bv)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление исправлено')
                return redirect('main:profile')
    else:
        form = BvForm(instance=bv)
        formset = AIFormSet(instance=bv)
    context = {'form':form, 'formset':formset}
    return render(request, 'main/profile_bv_change.html', context)

@login_required
def profile_bv_delete(request, pk):
    bv = get_object_or_404(Bv, pk=pk)
    if request.method == 'POST':
        bv.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect('main:profile')
    else:
        context = {'bv':bv}
        return render(request, 'main/profile_bv_delete.html', context)
        