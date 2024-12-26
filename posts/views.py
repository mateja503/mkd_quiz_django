from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin:posts_post_changelist')  # Redirect to admin page
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.all()  # Get all posts
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})

from django.shortcuts import render, get_object_or_404
from .models import Results

def results_list(request):
    results = Results.objects.all()  # Fetch all results
    return render(request, 'posts/results_list.html', {'results': results})

def result_detail(request, result_id):
    result = get_object_or_404(Results, id=result_id)  # Fetch the result by ID
    contestants = result.contestants.all()  # Get all contestants associated with this result
    return render(request, 'posts/result_detail.html', {'result': result, 'contestants': contestants})


import openpyxl
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contestant, Results
from .forms import ExcelUploadForm

@staff_member_required
def import_results_from_excel(request, result_id):
    # Try to get the result. If it doesn't exist, redirect to create result page
    try:
        result = Results.objects.get(id=result_id)
    except Results.DoesNotExist:
        return redirect('create_result')  # Redirect to the create result page

    if request.method == 'POST' and request.FILES['file']:
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']

            # Open the uploaded Excel file
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            # Iterate through the rows in the Excel sheet
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping header row
                name, surname, points = row

                # Create a new contestant and link it to the result
                contestant = Contestant.objects.create(
                    name=name,
                    surname=surname,
                    points=points
                )
                result.contestants.add(contestant)  # Add contestant to result

            return HttpResponse(f"Results for contest '{result.title}' imported successfully!")

    else:
        form = ExcelUploadForm()

    return render(request, 'posts/import_results.html', {'form': form, 'result': result})


from django.shortcuts import render, redirect
from .models import Results
from .forms import ResultForm


@staff_member_required
def create_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()  # Save the new result
            return redirect('results_list')  # Redirect to results list after creating
    else:
        form = ResultForm()

    return render(request, 'posts/create_result.html', {'form': form})