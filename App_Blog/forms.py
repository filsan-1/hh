from django import forms
from App_Blog.models import Blog, Comment, Recipe

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...'
            })
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_title', 'description', 'ingredients', 'instructions', 'servings', 'prep_time', 'cook_time', 'recipe_image')
        widgets = {
            'recipe_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe Title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the recipe',
                'required': True
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'List ingredients (one per line)\nExample:\n1 cup flour\n2 eggs\n1/2 cup sugar',
                'required': True
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Step-by-step cooking instructions (one step per line)\nExample:\nPreheat oven to 350°F\nMix dry ingredients\nAdd wet ingredients',
                'required': True
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 1,
                'value': 4
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 0,
                'placeholder': 'Minutes',
                'value': 15
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 0,
                'placeholder': 'Minutes',
                'value': 30
            }),
            'recipe_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


