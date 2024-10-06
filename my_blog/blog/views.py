from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from .models import Post


@method_decorator(cache_page(timeout=60))
class PostListView(ListView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments_count = cache.get(f'comments_count_{post.id}')
        if comments_count is None:
            comments_count = post.comments.count()
            cache.set(f'comments_count_{post.id}', comments_count, 300)
        context['comments_count'] = comments_count
        return context

    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related('comments')

        # SELECT "blog_post"."id", "blog_post"."title", "blog_post"."content", "blog_post"."author_id",
        # "blog_post"."created_date", "blog_user"."id", "blog_user"."password", "blog_user"."last_login",
        # "blog_user"."is_superuser", "blog_user"."username", "blog_user"."first_name", "blog_user"."last_name",
        # "blog_user"."email", "blog_user"."is_staff", "blog_user"."is_active", "blog_user"."date_joined",
        # "blog_user"."bio" FROM "blog_post" INNER JOIN "blog_user" ON ("blog_post"."author_id" = "blog_user"."id")

        return queryset