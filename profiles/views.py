from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from . import services
from .models import BookmarkedProfile


def jsearch(request):
    query = request.GET.get("q", "").strip()

    context = {
        "query": query,
        "profile": None,
        "repos": [],
    }

    if query:
        try:
            context["profile"] = services.get_user(query)

            context["repos"] = services.get_repos(
                context["profile"]["username"]
            )

        except services.GitHubError as exc:
            messages.error(request, str(exc))

    return render(request, "profiles/search.html", context)


@login_required
@require_POST
def bookmark(request, username):
    try:
        data = services.get_user(username)

    except services.GitHubError as exc:
        messages.error(request, str(exc))
        return redirect("search")

    lookup = data.pop("username")

    _, created = BookmarkedProfile.objects.get_or_create(
        user=request.user,
        username=lookup,
        defaults=data,
    )

    if created:
        messages.success(request, f"Bookmarked {lookup}.")

    else:
        messages.info(request, f"{lookup} is already bookmarked.")

    return redirect("bookmarks")


@login_required
def bookmark_list(request):
    items = BookmarkedProfile.objects.filter(
        user=request.user
    )

    return render(
        request,
        "profiles/bookmarks.html",
        {"bookmarks": items},
    )


@login_required
@require_POST
def bookmark_delete(request, pk):
    item = get_object_or_404(
        BookmarkedProfile,
        pk=pk,
        user=request.user,
    )

    item.delete()

    messages.success(request, "Bookmark removed.")

    return redirect("bookmarks")

from django.http import HttpResponseBadRequest,FileResponse,HttpResponse
from .temp import render_and_return_image
import io
def visualize(request):
    username=request.GET.get("username","").strip()
    if not username:
        return HttpResponseBadRequest("Missing username parameter.")

    try:
        profile=services.get_user(username)
        repos=services.get_repos(username)
        img= render_and_return_image(username=profile['username'],
                         name=profile['name'],
                         bio=profile['name'],
                         public_repos=profile['public_repos'],
                         followers=profile['followers'],
                         )
    except services.GitHubError as exc:
        return HttpResponseBadRequest(str(exc))
    buffer=io.BytesIO()
    img.save(buffer,format="PNG")
    buffer.seek(0)
    return FileResponse(buffer,content_type="image/png")


def search(request):
    query = request.GET.get("q", "").strip()

    context = {
        "query": query,
        "profile": None,
        "repos": [],
    }

    if query:
        try:
            context["profile"] = services.get_user(query)

            context["repos"] = services.get_repos(
                context["profile"]["username"]
            )

        except services.GitHubError as exc:
            messages.error(request, str(exc))

    return JsonResponse(context)