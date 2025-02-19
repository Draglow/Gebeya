from django.shortcuts import render
from core.models import Post,ReplyComment,Comment,ReplyComment,Notification
import shortuuid
from django.utils.text import slugify
from django.http import JsonResponse
from django.utils.timesince import timesince
from  django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.defaultfilters import timesince
from django.contrib.auth.decorators import login_required
from userauths.models import User

from django.db.models import OuterRef,Subquery,Q

# Create your views here.
noti_new_like="New Like"
noti_new_follower="New Followers"

noti_new_comment="New Comment"
noti_comment_liked="Comment Liked"
noti_comment_replied="Comment Replied"


def send_notification(user=None,sender=None,post=None,comment=None,notification_type=None):
    notification=Notification.objects.create(
        user=user,
        sender=sender,
        post=post,
        comment=comment,
        notification_type=notification_type,
    )
    
    return notification
@login_required
def post_detail(request,slug):
    posts=Post.objects.get(slug=slug,visibility='Everyone',active=True)
    context={
        'posts':posts
    }
    
    return render(request,'core/detail.html',context)
@login_required
def index(request):
    posts=Post.objects.filter(active=True,visibility='Everyone').order_by('-id')
    
    context={
        'postss':posts,
        
    }
    return render(request,'core/index.html',context)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')
        
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        
        if title and image:
            post = Post(
                title=title,
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            post.save()
            
            # Calculate time difference using current time if post.date is None
            current_time = timezone.now()
            post_date = post.date if post.date is not None else current_time
            time_difference = timesince(post_date)
            
            # Convert ImageFieldFile to string representation of image URL
            image_url = post.image.url if post.image else ''

            return JsonResponse({
                'post': {
                    'title': post.title,
                    'image': image_url,
                    'full_name': post.user.profile.full_name,
                    'profile_image': post.user.profile.image.url,
                    'date': time_difference,
                    'id': post.id
                }
            })
        
        else:
            return JsonResponse({'error': 'image or title does not exist'})
    
    return JsonResponse({'data': 'sent'})

def like_post(request):
    id = request.GET.get('id')
    post = Post.objects.get(id=id)
    user = request.user
    bool_val = False
    
    if user in post.likes.all():
        post.likes.remove(user)
    
    else:
        post.likes.add(user)
        bool_val = True
    
    post.save()  # Save the changes to the post

    if post.user != request.user:
        send_notification(post.user,user,post,None,noti_new_like)
    
    data = {
        'bool': bool_val,
        'likes': post.likes.all().count()
    }
    
    return JsonResponse({'data': data})

def comment_on_post(request):
    id=request.GET['id']
    comment=request.GET['comment']
    post=Post.objects.get(id=id)
    comment_count=Comment.objects.filter(post=post).count()
    user=request.user
    
    new_comment=Comment.objects.create(
        post=post,
        comment=comment,
        user=user
    )
    
    if new_comment.user != post.user:
        send_notification(post.user,user,post,new_comment,noti_new_comment)
    
    
    data = {
        "bool": True,
        "comment": new_comment.comment,
        "profile_image":new_comment.user.profile.image.url,
        "user_id": new_comment.user.id,
        "date": timesince(new_comment.date),
        "comment_id": new_comment.id,
        "post_id": new_comment.post.id,
        "comment_count": comment_count +int(1)
}

    
    return JsonResponse({'data': data})

def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False
    
    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool= True

    if comment.user != user:
        send_notification(comment.user,user,comment.post,comment,noti_comment_liked)
    
    
    data = {
        'bool': bool,
        'likes': comment.likes.all().count()
    }
    
    return JsonResponse({'data': data})

from django.core.serializers import serialize
from django.http import JsonResponse
from django.template.defaultfilters import timesince
from django.db.models.fields.files import ImageFieldFile

def reply_comment(request):
    id = request.GET.get('id')
    reply = request.GET.get('reply')
    comment = Comment.objects.get(id=id)
    user = request.user
    
    new_reply = ReplyComment.objects.create(
        comment=comment,
        reply=reply,
        user=user
    )
    if comment.user != user:
        send_notification(comment.user,user,comment.post,comment,noti_comment_replied)
    
    data = {
        "bool": True,
        "reply": new_reply.reply,
        "profile_image": new_reply.user.profile.image.url,
        "user_id": new_reply.user.id,
        "date": timesince(new_reply.date),
        "reply_id": new_reply.id,
        "post_id": new_reply.comment.post.id,
    }
    
    return JsonResponse({'data': data})

def delete_comment(request):
    id=request.GET['id']
    comment=Comment.objects.filter(id=id)
    comment.delete()
    
    data={
        'bool':True,
        
    }
    
    return JsonResponse({'data': data})


def delete_reply(request):
    id=request.GET['id']
    reply=ReplyComment.objects.filter(id=id)
    reply.delete()
    
    data={
        'bool':True,
        
    }
    
    return JsonResponse({'data': data})



