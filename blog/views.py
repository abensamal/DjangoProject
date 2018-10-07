from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Comments
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from .forms import CommentForm
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.template.context_processors import csrf
from django.contrib import auth
from django.shortcuts import redirect



# Create your views here.


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if not request.user.is_authenticated():
        raise  Http404
    
    if request.user.is_staff or request.user.is_superuser:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
        #print form.cleaned_data.get("title")
            instance.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form" : form,
    }
    return render(request, "post_form.html", context)
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    # if not request.user.is_authenticated():
    #     raise  Http404
    # form = PostForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.author = request.user
    #     #print form.cleaned_data.get("title")
    #     instance.save()
    #     messages.success(request, "Successfully Created")
    #     return HttpResponseRedirect(instance.get_absolute_url())

    # context = {
    #     "form" : form,
    # }
    # return render(request, "post_form.html", context)

def post_detail(request, id=None):
    comment_form = CommentForm

    #instance = Post.object.get(id = 1)
    instance = get_object_or_404(Post, id=id)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.text)
    context = {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string,
        "form1" : comment_form,
        "comments" : Comments.objects.filter(comment_post_id=id),
        "username" : auth.get_user(request).username,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()#filter(draft=False).filter(publish__lte=timezone.now())#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)

        ).distinct()
    paginator = Paginator(queryset_list, 4)
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title" : "List",
        "object_list" :queryset,
        # "page_request_var": page_request_var,
        "today" : today,
        "username" : auth.get_user(request).username,
    }
    return render(request, "post_list.html", context)

def addlike(request, id):
    if request.user.is_authenticated:
        try:
            if id in request.COOKIES:
                redirect('/posts')
            else:
                post = get_object_or_404(Post, id=id)
                post.likes += 1
                post.save()
                response = redirect('/posts')
                response.set_cookie(id, "test")
                return response
        except ObjectDoesNotExist:
            raise Http404
        return redirect('/posts')
    else: 
        return redirect('/posts')
    #return HttpResponseRedirect(post.get_absolute_url())
# def addlike(request, id):
#     try:
#          # if pk in request.COOKIES:
#          #     redirect('/')
#          # else:
#             post = Post.objects.get(id=id)
#             post.likes += 1
#             post.save()
#             # response = redirect('/')
#             # response.set_cookie(pk, "test")
#             # return response
#     except ObjectDoesNotExist:
#         raise Http404
#     return redirect(request, "post_list.html")
def addcomment(request, id):
    post = Post.objects.get(id=id)
    if request.POST and ("pause" not in request.session):

        form1=CommentForm(request.POST)
        if form1.is_valid():
            comment =form1.save(commit=False)
            comment.comment_post=Post.objects.get(id=id)
            form1.save()
            request.session.set_expiry(60)
            request.session['pause'] =True
    return HttpResponseRedirect(post.get_absolute_url())
    # return render(request, 'post_detail.html', id= id)

def post_update(request, id=None):
    if not request.user.is_authenticated:
    # if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance = instance)
    if form.is_valid():
        instance =form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title" : instance.title,
        "instance" : instance,
        "form" : form,
    }
    return render(request, "post_form.html", context)

def post_delete(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    return HttpResponse("<h1>Delete</h1>")