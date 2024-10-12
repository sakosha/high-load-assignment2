from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from .models import Post


@method_decorator(cache_page(timeout=60), name='dispatch')
class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'post_list.html'
    # sanzhar
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = context['object_list']
        comments_count_dict = {}

        for post in post_list:
            comments_count = cache.get(f'comments_count_{post.id}')
            if comments_count is None:
                comments_count = post.comments.count()
                cache.set(f'comments_count_{post.id}', comments_count, 300)
            comments_count_dict[post.id] = comments_count

        context['comments_count_dict'] = comments_count_dict
        return context

    def get_queryset(self):
        # SELECT
        # "blog_post"."id", "blog_post"."title", "blog_post"."content",
        # "blog_post"."author_id", "blog_post"."created_date", "blog_user"."id",
        # "blog_user"."password", "blog_user"."last_login", "blog_user"."is_superuser",
        # "blog_user"."username", "blog_user"."first_name", "blog_user"."last_name",
        # "blog_user"."email", "blog_user"."is_staff", "blog_user"."is_active",
        # "blog_user"."date_joined", "blog_user"."bio"
        # FROM "blog_post"
        # INNER JOIN "blog_user"
        # ON ("blog_post"."author_id" = "blog_user"."id")

        return Post.objects.select_related('author').prefetch_related(
            'comments'
        )


def health_check(request):
    return JsonResponse({'status': 'ok'}, status=200)
