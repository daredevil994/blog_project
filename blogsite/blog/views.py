from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post, Comment
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.contrib.auth import login,authenticate,logout
from django.views.generic import (TemplateView,
                                ListView,DetailView,
                                CreateView,
                                UpdateView,DeleteView
                                )

# Create your views here.

class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model= Post

    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')

class PostDetailView(DetailView):
    model=Post

    # def get_context_data(self,pk):
    #     post=get_object_or_404(Post,pk=pk)
    #     context=super().get_context_data(post.text)
    #
    #     return context


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class= PostForm
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class= PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_draft_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('create_date')

#########################################################################
def index(request):
    return render(request,'blog/about.html')

# @login_required
# def confirm_delete(request,pk):


@login_required
def publish_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form=CommentForm()
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def remove_comment(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                 login(request,user)
                 return render(request,'about.html')
            else:
                HttpResponse('Account Not Active Anymore')
        else:
            print("Worng login activity!")
            print("Username: {} and Password: {}".format(username,password))
            return render(request,'login.html',{'msg':"invalid username and password!"})
    else:
        return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request,'login.html')
