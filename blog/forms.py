from django import forms
from .models import Post
from .models import Comments

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "speciality",
            "text",
            "image",
            "draft",
            "publish",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comments
        fields=['comment_text']



 
 
# class CommentForm(forms.Form):
 
#     parent_comment = forms.IntegerField(
#         widget=forms.HiddenInput,
#         required=False
#     )
 
#     comment_area = forms.CharField(
#         label="",
#         widget=forms.Textarea
#     )