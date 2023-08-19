import datetime

from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView
)
from django.db import transaction
from django.urls import reverse_lazy, reverse

from blog.models import Post, Comment, Category
from blog.forms import PostForm, CommentForm, ProfileUpdateForm


class ProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('username'):
            context['profile'] = get_user_model().objects.get(
                username=self.kwargs['username']
                )
            paginator = Paginator(
                self.object.posts.select_related('author').
                order_by('-pub_date').
                annotate(comment_count=Count('comments')),
                10
                )
            context['page_obj'] = paginator.get_page(
                self.request.GET.get('page')
                )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:profile')
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = ProfileUpdateForm(
                self.request.POST, instance=self.request.user
            )
        else:
            context['user_form'] = ProfileUpdateForm(
                instance=self.request.user
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.username}
                            )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=datetime.datetime.now()
            ).annotate(comment_count=Count('comments'))


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
             self.object.comments.select_related('post').order_by('created_at')
        )
        return context


class CategoryDetailView(DetailView):
    model = Category
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('slug'):
            context['category'] = get_object_or_404(
                Category,
                slug=self.kwargs['slug'], is_published=True
                )
            paginator = Paginator(
                self.object.posts.select_related('category').
                filter(
                    is_published=True,
                    category__is_published=True,
                    pub_date__lte=datetime.datetime.now()
                    ), 10
                )
            context['page_obj'] = paginator.get_page(
                self.request.GET.get('page')
                )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_object = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_object.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['post_id'])
        comment_object = get_object_or_404(
                    Comment,
                    post=self.post_object,
                    id=self.kwargs['comment_id']
                    )
        if comment_object.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('post_id'):
            post_object = get_object_or_404(
                Post, id=self.kwargs['post_id']
                )
            if self.kwargs.get('comment_id'):
                context['comment'] = get_object_or_404(
                    Comment,
                    post=post_object,
                    id=self.kwargs['comment_id']
                    )
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_object.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['post_id'])
        comment_object = get_object_or_404(
                    Comment,
                    post=self.post_object,
                    id=self.kwargs['comment_id']
                    )
        if comment_object.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('post_id'):
            post_object = get_object_or_404(
                Post, id=self.kwargs['post_id']
                )
            if self.kwargs.get('comment_id'):
                context['comment'] = get_object_or_404(
                    Comment,
                    post=post_object,
                    id=self.kwargs['comment_id']
                    )
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_object.pk})
