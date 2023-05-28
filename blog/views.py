from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.template.loader import get_template
from django.views.generic import ListView
from xhtml2pdf import pisa

from .forms import NewCommentForm, PostSearchForm
from .models import Category, Post


def home(request):
    posts = Post.newmanager.all()
    context = {"posts": posts}
    return render(request, "blog/index.html", context)


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status="published")

    fav = bool

    if post.favourites.filter(id=request.user.id).exists():
        fav = True

    allcomments = post.comments.filter(status=True)
    page = request.GET.get("page", 1)
    paginator = Paginator(allcomments, 4)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    comment_form = NewCommentForm(request.POST or None)
    if request.method == "POST":
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect("/" + post.slug)
        else:
            comment_form = NewCommentForm()
    context = {
        "post": post,
        "comments": user_comment,
        "comments": comments,
        "comment_form": comment_form,
        "allcomments": allcomments,
        "fav": fav,
    }
    return render(request, "blog/single.html", context)


class CatListView(ListView):
    template_name = "blog/category.html"
    context_object_name = "catlist"

    def get_queryset(self):
        content = {
            "cat": self.kwargs["category"],
            "posts": Post.objects.filter(category__name=self.kwargs["category"]).filter(
                status="published"
            ),
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name="default")
    context = {"category_list": category_list}

    return context


def post_search(request):
    form = PostSearchForm()
    q = ""
    c = ""
    results = []
    query = Q()

    if request.POST.get("action") == "post":
        search_string = str(request.POST.get("ss"))

        if search_string is not None:
            search_string = Post.objects.filter(title__icontains=search_string)[:5]
            data = serializers.serialize(
                "json", list(search_string), fields=("id", "title", "slug")
            )
            return JsonResponse({"search_string": data})

    if "q" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]
            c = form.cleaned_data["c"]

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__icontains=q)

            results = Post.objects.filter(query)

    context = {"form": form, "q": q, "c": c, "results": results}
    return render(request, "blog/search.html", context)


def post_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    post = get_object_or_404(Post, pk=pk)
    template_path = "blog/pdf_template.html"
    context = {"post": post}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="excession-post.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


def contact(request):
    context = {}
    return render(request, "blog/contact.html", context)


def about(request):
    context = {}
    return render(request, "blog/about.html", context)
