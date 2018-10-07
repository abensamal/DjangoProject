
from __future__ import unicode_literals
from django.conf import  settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
# Create your models here.
#model view controller-MVC

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" % (instance.id , filename)
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" % (instance.id , instance.id, extension)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               default=1)
    title = models.CharField(max_length = 200)
    speciality = models.IntegerField()
    image = models.ImageField(upload_to= upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.IntegerField(default=0)

    objects = PostManager()


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id" : self.id } )
        #return "/posts/%s/" %(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]



# class Comment(models.Model):
#     class Meta:
#         db_table = "comments"
 
#     path = ArrayField(models.IntegerField())
#     post_id = models.ForeignKey(Article)
#     author_id = models.ForeignKey(User)
#     content = models.TextField('Комментарий')
#     pub_date = models.DateTimeField('Дата комментария', default=timezone.now)
 
#     def __str__(self):
#         return self.content[0:200]
 
#     def get_offset(self):
#         level = len(self.path) - 1
#         if level > 5:
#             level = 5
#         return level
 
#     def get_col(self):
#         level = len(self.path) - 1
#         if level > 5:
#             level = 5
#         return 12 - level

class Comments(models.Model):
    # comment_author =
    # comment_user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
    #comment_date=models.DateTimeField(auto_now=True)
    comment_text = models.TextField(verbose_name = "Comment text:")
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)