import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follows, Like

def index(request):
    raw_posts = Post.objects.all().order_by("-upload_date")
    posts =[]
    user = request.user
    if user.is_authenticated:
        for p in raw_posts:
            if Like.objects.filter(liker=user, liked_post=p.post_id).exists():
                posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, True])
            else:
                posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, False])
    else:
        for p in raw_posts:
            posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, False])
    
    pagination = Paginator(posts, 10)
    page_num = request.GET.get('page')
    posts = pagination.get_page(page_num)
    return render(request, "network/index.html", {
        "posts": posts,
        "num_pages": range(1, posts.paginator.num_pages+1)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="/login")
def new_post(request):
    if request.method == "GET":
        return render(request, "network/new_post.html")
    
    content = request.POST.get("content")
    title = request.POST.get("title")
    new = Post(poster=request.user, title=title, content=content, upload_date=timezone.now())
    new.save()
    return redirect(reverse("index"))


def see_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    followers = Follows.objects.filter(followed=user).count()
    following = Follows.objects.filter(follower=user).count()
    being_followed = False
    if request.user.is_authenticated:
        if Follows.objects.filter(followed=user, follower=request.user).exists():
            being_followed = True

    raw_posts = Post.objects.filter(poster=user).order_by("-upload_date")
    posts =[]
    getter = request.user
    if getter.is_authenticated:
        for p in raw_posts:
            if Like.objects.filter(liker=getter, liked_post=p.post_id).exists():
                posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, True])
            else:
                posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, False])
    else:
        for p in raw_posts:
            posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, False])
    
    pagination = Paginator(posts, 10)
    page_num = request.GET.get('page')
    posts = pagination.get_page(page_num)
    
    return render(request, "network/user_prof.html", {
        "posts": posts,
        "userp": user,
        "followers": followers,
        "following": following,
        "being_followed": being_followed,
        "num_pages": range(1, posts.paginator.num_pages+1)
    })


@login_required(login_url="/login")
def following_page(request):
    following = Follows.objects.filter(follower=request.user)
    posts = []
    for follow in following:
        raw_posts = Post.objects.filter(poster=follow.followed).order_by("-upload_date")
        for p in raw_posts:
            if Like.objects.filter(liker=request.user, liked_post=p.post_id).exists():
                posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, True])
            else:
                posts.append([p.post_id, p.poster, p.title, p.content, p.upload_date, p.likes, False])

    pagination = Paginator(posts, 10)
    page_num = request.GET.get('page')
    posts = pagination.get_page(page_num)
    return render(request, "network/following.html", {
        "posts": posts,
        "num_pages": range(1, posts.paginator.num_pages+1)
    })


@csrf_exempt
def edit_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request allowed only", "status": 400}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Must be logged in to like/unlike posts", "status": 401}, status=401)

    data = json.loads(request.body)
    edited_content = data.get("edited_data")
    post_id = data.get("post_id")
    relevant_post = Post.objects.filter(post_id=post_id).first()
    if relevant_post.poster != request.user:
        return JsonResponse({"error": "You cannot edit another person's post", "status": 401}, status=403)

    relevant_post.content = edited_content
    relevant_post.save(update_fields=["content"])
    return JsonResponse({"message": "Post updated"}, status=200)
    

@csrf_exempt
def like_unlike(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request allowed only", "status": 400}, status=400)
    
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Must be logged in to like/unlike posts", "status": 401}, status=401)

    data = json.loads(request.body)
    action = data.get("action")
    post_id = data.get("post_id")
    relevant_post = Post.objects.filter(post_id=post_id).first()
    if action == "like":
        new_like = Like(liker=request.user, liked_post=relevant_post)
        new_like.save()
        relevant_post.likes += 1
        relevant_post.save(update_fields=["likes"])
        return JsonResponse({
                "message": "liked",
                "likes": relevant_post.likes,
                "status": 200
            }, status=200)
    else:
        try:
            Like.objects.filter(liker=request.user, liked_post=relevant_post).delete()
            relevant_post.likes -= 1
            relevant_post.save(update_fields=["likes"])
            return JsonResponse({
                    "message": "unliked",
                    "likes": relevant_post.likes,
                    "status": 200
                }, status=200)
        except:
            return JsonResponse({
                    "message": "no change made",
                    "likes": relevant_post.likes,
                    "status": 200
                }, status=200)


@csrf_exempt
def followstuff(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request allowed only", "status": 400}, status=400)
    
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Must be logged in to follow/unfollow users", "status": 401}, status=401)

    data = json.loads(request.body)
    action = data.get("action").lower()
    if action not in ["follow", "unfollow"]:
        return JsonResponse({"error": "Invalid action", "status": 400}, status=400)

    followee_id = data.get("followee")
    followee = User.objects.filter(id=followee_id).first()
    if not followee:
        return JsonResponse({"error": "Invalid user id", "status": 400}, status=400)

    follower = request.user
    if action == "follow":
        if not Follows.objects.filter(follower=follower, followed=followee).exists():
            Follows.objects.create(follower=follower, followed=followee)
        num_followers = Follows.objects.filter(followed=followee).count()
        num_following = Follows.objects.filter(follower=followee).count()
        return JsonResponse({"message": "following", "num_followers": num_followers, "num_followings": num_following}, status=200)

    else:
        if Follows.objects.filter(follower=follower, followed=followee).exists():
            Follows.objects.filter(follower=follower, followed=followee).delete()
        num_followers = Follows.objects.filter(followed=followee).count()
        num_following = Follows.objects.filter(follower=followee).count()
        return JsonResponse({"message": "unfollowed", "num_followers": num_followers, "num_followings": num_following}, status=200)