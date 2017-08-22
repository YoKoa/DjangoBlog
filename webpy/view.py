#from django.http import HttpResponse
from CountryInfo.models import *
from CountryInfo.froms import CommentForm
from django.http import Http404
from django.shortcuts import render,render_to_response
def hello(request):
    context={}
    context['hello'] ='world'
    return render(request,'hello.html',context)
def get_blogs(request):
    blogs = Blog.objects.all().order_by('-created')
    return render_to_response('blog_list.html', {'blogs': blogs})
def get_details(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)
    ctx = {
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-created'),
        'form': form
    }
    return render(request, 'blog_details.html', ctx)