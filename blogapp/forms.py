from django import forms
from .models import Post,News
import datetime


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postname', 'content', 'category', 'image']

        widgets = {
            'postname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your content here...'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

        labels = {
            'postname': 'Post Title',
            'content': 'Content',
            'category': 'Category',
            'image': 'Featured Image'
        }

    def clean_postname(self):
        postname = self.cleaned_data.get('postname')
        if len(postname) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return postname

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError("Content must be at least 50 characters long.")
        return content

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only JPG, JPEG or PNG img allowed")
        return image
    
    
class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        fields='__all__'
        
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the news title'}),
            'type_of_news':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the type of news'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter description'}),
            
        }
        
        
        
         