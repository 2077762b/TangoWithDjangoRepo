from django.shortcuts import render
from rango_app.models import Category
from rango_app.models import Page
from rango_app.forms import CategoryForm
from rango_app.forms import PageForm

from django.http import HttpResponse

def index(request):
   
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,'pages':page_list}
    return render(request, 'rango/index.txt', context_dict)

def about(request):
    context_dict = {'name': "Chris Brown", 'number': "2077762b" }
    return render(request, 'rango/about.txt', context_dict)

def category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.txt', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
		
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.txt', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return index(request)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'category_name_slug':category_name_slug }

    return render(request, 'rango/add_page.txt', context_dict)
