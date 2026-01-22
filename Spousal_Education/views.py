from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Q, Count
from django.contrib import messages as django_messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import EducationalArticle, ArticleCategory, ArticleLike, ArticleBookmark, ArticleComment
from .forms import ArticleCommentForm


def article_list(request):
    """Display list of all educational articles"""
    articles = EducationalArticle.objects.filter(is_published=True)
    categories = ArticleCategory.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(ArticleCategory, slug=category_slug)
        articles = articles.filter(category=category)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        articles = articles.filter(difficulty_level=difficulty)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Sort
    sort_by = request.GET.get('sort', '-published_date')
    if sort_by == 'popular':
        articles = articles.order_by('-views_count', '-likes_count')
    elif sort_by == 'newest':
        articles = articles.order_by('-published_date')
    elif sort_by == 'oldest':
        articles = articles.order_by('published_date')
    
    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    
    # Featured articles
    featured_articles = EducationalArticle.objects.filter(is_published=True, featured=True)[:3]
    
    context = {
        'articles': articles_page,
        'categories': categories,
        'featured_articles': featured_articles,
        'page_title': 'Spousal Education - Understanding Women\'s Health',
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'search_query': search_query,
    }
    return render(request, 'Spousal_Education/article_list.html', context)


def article_detail(request, slug):
    """Display detailed view of an article"""
    article = get_object_or_404(EducationalArticle, slug=slug, is_published=True)
    
    # Increment view count
    article.increment_views()
    
    # Check if user has liked or bookmarked
    user_has_liked = False
    user_has_bookmarked = False
    if request.user.is_authenticated:
        user_has_liked = ArticleLike.objects.filter(article=article, user=request.user).exists()
        user_has_bookmarked = ArticleBookmark.objects.filter(article=article, user=request.user).exists()
    
    # Comments
    comments = article.comments.filter(is_approved=True)
    comment_form = ArticleCommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = ArticleCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            django_messages.success(request, 'Your comment has been posted!')
            return redirect('Spousal_Education:article_detail', slug=article.slug)
    
    # Related articles
    related_articles = EducationalArticle.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id)[:3]
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'related_articles': related_articles,
        'user_has_liked': user_has_liked,
        'user_has_bookmarked': user_has_bookmarked,
        'page_title': article.title,
    }
    return render(request, 'Spousal_Education/article_detail.html', context)


def category_list(request):
    """Display all categories"""
    categories = ArticleCategory.objects.annotate(
        article_count=Count('articles', filter=Q(articles__is_published=True))
    )
    
    context = {
        'categories': categories,
        'page_title': 'Article Categories',
    }
    return render(request, 'Spousal_Education/category_list.html', context)


@login_required
@require_POST
def toggle_like(request, slug):
    """Toggle like on an article"""
    article = get_object_or_404(EducationalArticle, slug=slug)
    
    like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
    
    if not created:
        like.delete()
        article.likes_count -= 1
        article.save(update_fields=['likes_count'])
        liked = False
    else:
        article.likes_count += 1
        article.save(update_fields=['likes_count'])
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': article.likes_count
        })
    
    return redirect('Spousal_Education:article_detail', slug=article.slug)


@login_required
@require_POST
def toggle_bookmark(request, slug):
    """Toggle bookmark on an article"""
    article = get_object_or_404(EducationalArticle, slug=slug)
    
    bookmark, created = ArticleBookmark.objects.get_or_create(article=article, user=request.user)
    
    if not created:
        bookmark.delete()
        bookmarked = False
        message = 'Article removed from bookmarks'
    else:
        bookmarked = True
        message = 'Article bookmarked successfully!'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'bookmarked': bookmarked,
            'message': message
        })
    
    django_messages.success(request, message)
    return redirect('Spousal_Education:article_detail', slug=article.slug)


@login_required
def my_bookmarks(request):
    """Display user's bookmarked articles"""
    bookmarks = ArticleBookmark.objects.filter(user=request.user).select_related('article')
    
    context = {
        'bookmarks': bookmarks,
        'page_title': 'My Bookmarked Articles',
    }
    return render(request, 'Spousal_Education/my_bookmarks.html', context)


@login_required
@require_POST
def delete_comment(request, comment_id):
    """Delete a comment (only by comment author)"""
    comment = get_object_or_404(ArticleComment, id=comment_id)
    
    if comment.user == request.user or request.user.is_staff:
        article_slug = comment.article.slug
        comment.delete()
        django_messages.success(request, 'Comment deleted successfully.')
        return redirect('Spousal_Education:article_detail', slug=article_slug)
    
    django_messages.error(request, 'You do not have permission to delete this comment.')
    return redirect('Spousal_Education:article_detail', slug=comment.article.slug)
