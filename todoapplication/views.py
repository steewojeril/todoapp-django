from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,CreateView,DetailView,UpdateView,DeleteView
from todoapplication import forms
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from todoapplication.models import Todo
from django.contrib import messages
from django.urls import reverse_lazy
from todoapplication.decorators import sign_in_required
from django.utils.decorators import method_decorator
# class SignupView(View):
#     def get(self,request,*args,**kwargs):
#         form=forms.RegistrationForm()
#         return render(request,"registration.html",{'form':form})
        
#     def post(self,request,*args,**kwargs):
#    
#         form=forms.RegistrationForm(request.POST)
#         if form.is_valid():
#             User.objects.create_user(**form.cleaned_data)
#             messages.success(request,'Your Profile has been created!')
#             return redirect('login')
#         else:
#             messages.error(request,'Something went wrong')
#             return render(request,'registration.html',{'form':form})
class SignupView(CreateView):
    model=User
    form_class=forms.RegistrationForm
    template_name='registration.html'
    success_url=reverse_lazy('login')
    
class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                print('user:::',request.user)
                messages.success(request,'You have been successfully Logged in. Welcome %s' %request.user)
                return redirect('home')
            else:
                messages.error(request,'Incorrect username/password')
                return render(request,'login.html',{'form':form})
            
# class IndexView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,'index.html')
@method_decorator(sign_in_required,name='dispatch')
class IndexView(TemplateView):
    template_name='index.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['todo_incomplete']=Todo.objects.filter(user=self.request.user,status=False)
        return context
@method_decorator(sign_in_required,name='dispatch')
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'You have been succesfully logged out')
        return redirect('login')
    
# class TodoAddView(View):
#     def get(self,request,*args,**kwargs):
#         form=forms.TodoForm()
#         return render(request,'todoadd.html',{'form':form})
#     def post(self,request,*args,**kwargs):
#         form=forms.TodoForm(request.POST)
#         if form.is_valid():
#             form.instance.user=request.user
#             form.save()
#             messages.success(request,'Your todo has been added')
#             return redirect('home')
#         else:
#             messages.error(request,'Your todo has not been added')
#             return render('todoadd.html',{'form':form})
@method_decorator(sign_in_required,name='dispatch')
class TodoAddView(CreateView):
    model=Todo
    form_class=forms.TodoForm
    template_name='todoadd.html'
    success_url=reverse_lazy('home')

    def form_valid(self, form) :
        form.instance.user=self.request.user
        messages.success(self.request,'Your todo has been added!!!')
        return super().form_valid(form)
    


# class TodoListView(View):
#     def get(self,request,*args,**kwargs):
#         todos=Todo.objects.filter(user=request.user)
#         return render(request,'todolist.html',{'todos':todos})
@method_decorator(sign_in_required,name='dispatch')
class TodoListView(ListView):
    model=Todo
    context_object_name='todos'
    template_name='todolist.html'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
# @sign_in_required    
# def delete_todo(request,*args,**kwargs):
#     id=kwargs.get('id')
#     Todo.objects.get(id=id).delete()
#     messages.success(request,'Your todo has been deleted')

#     return redirect('todolist')

@method_decorator(sign_in_required,name='dispatch')
class DeleteTodo(DeleteView):
    model=Todo
    pk_url_kwarg='id'
    success_url=reverse_lazy('todolist')
    template_name='tododelete.html'
    def get_success_url(self):
        from_page = self.request.GET.get('from_page', '')
        if from_page == 'home':
            return reverse_lazy('home')
        return reverse_lazy('todolist')

# class TodoDetailView(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get('id')
#         todo=Todo.objects.get(id=id)
#         return render(request,'tododetails.html',{'todo':todo})
@method_decorator(sign_in_required,name='dispatch')
class TodoDetailView(DetailView):
    model=Todo
    # context_object_name='todo'
    template_name='tododetails.html'
    pk_url_kwarg='id'

# class TodoEditView(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get('id')
#         todo=Todo.objects.get(id=id)
#         form=forms.TodoEditForm(instance=todo)
#         return render(request,'todoedit.html',{'form':form})
#     def post(self,request,*args,**kwargs):
#         id=kwargs.get('id')
#         todo=Todo.objects.get(id=id)
#         form=forms.TodoEditForm(request.POST,instance=todo)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Your todo has been edited')
#             return redirect('todolist')
#         else:
#             messages.error(request,'something went wrong! Try again')
#             return render(request,'todoedit.html',{'form':form})
@method_decorator(sign_in_required,name='dispatch')
class TodoEditView(UpdateView):
    model=Todo
    fields=['task_name','status']
    form=forms.TodoEditForm
    template_name='todoedit.html'
    pk_url_kwarg='id'
    # success_url=reverse_lazy('todolist')

    def get_success_url(self):
        from_page = self.request.GET.get('from_page', '')
        if from_page == 'home':
            return reverse_lazy('home')
        return reverse_lazy('todolist')
    