from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def video_view(request, video_number):
    # Define the videos URLs in a dictionary or list
    videos = [
        "rHux0gMZ3Eg",
        "kqtD5dpn9C8",
        "eow125xV5-c",  
        "PRSyHTajxPk",
        "OEV8gMkCHXQ"
    ]
    
    # Ensure the video number is within the valid range
    video_number = max(1, min(video_number, 5))  # Clamp between 1 and 5
    
    # Get the previous and next video numbers
    prev_number = video_number - 1 if video_number > 1 else video_number
    next_number = video_number + 1 if video_number < 5 else video_number
    
    # Get the selected video URL
    selected_video = videos[video_number - 1]
    
    context = {
        'video_number': selected_video,
        'prev_number': prev_number,
        'next_number': next_number
    }
    
    return render(request, 'blog/video.html', context)



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
