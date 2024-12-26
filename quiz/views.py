from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import QuizResult
from django.utils.timezone import localtime

questions = [
    {'id': 1, 'question_text': 'What is 2 + 2?', 'choice_1': '3', 'choice_2': '4', 'choice_3': '5', 'choice_4': '6',
     'correct_answer': '2'},
    {'id': 2, 'question_text': 'What is the capital of France?', 'choice_1': 'London', 'choice_2': 'Paris',
     'choice_3': 'Berlin', 'choice_4': 'Madrid', 'correct_answer': '2'},
]

from django.shortcuts import render, redirect
from .models import Question
import random

# views.py
from django.shortcuts import render, redirect
from .models import Question
import random

from django.shortcuts import render, redirect
from .models import Question
from random import sample


def start_quiz(request):
    # Initialize score in session if not already set
    request.session['score'] = 0
    request.session['lifeline_used'] = False  # Reset lifeline usage for a new quiz

    # Handle the category and difficulty selection
    if request.method == "POST":
        # Get the selected category and difficulty from the form, defaulting to "Mixed"
        category = request.POST.get('category', 'Mixed')
        difficulty = request.POST.get('difficulty', 'Mixed')

        # Store the selected category and difficulty in session
        request.session['category'] = category
        request.session['difficulty'] = difficulty

        # Filter questions based on category and difficulty, using "Mixed" as default for both
        questions = Question.objects.all()

        if category != 'Mixed':
            questions = questions.filter(category=category)

        if difficulty != 'Mixed':
            questions = questions.filter(difficulty=difficulty)

        # Ensure at least 2 questions are available to choose from
        if len(questions) < 2:
            return render(request, 'quiz/no_questions.html')  # Handle case when not enough questions are available

        # Randomly select 2 questions
        selected_questions = sample(list(questions), 2)  # Ensure randomness

        # Store the question IDs in session for tracking
        request.session['question_ids'] = [q.id for q in selected_questions]

        # Redirect to the first question
        first_question = selected_questions[0]
        return redirect('quiz:question', question_id=first_question.id)

    # If the request method is GET, display the form to select category and difficulty
    categories = ['Science', 'History', 'General Knowledge', 'Art', 'Sport']
    difficulties = ['Easy', 'Medium', 'Hard']

    return render(request, 'quiz/start_quiz.html', {
        'categories': categories,
        'difficulties': difficulties
    })


@login_required
def quiz(request):
    score = 0
    total = len(questions)

    if request.method == 'POST':
        # Calculate the user's score
        for question in questions:
            user_answer = request.POST.get(f'question_{question["id"]}')
            if user_answer == question['correct_answer']:
                score += 1

        # Save the result to the database
        QuizResult.objects.create(user=request.user, score=score)

    return render(request, 'quiz/quiz.html', {
        'questions': questions,
        'score': score,
        'total': total,
    })
import random
from django.shortcuts import render, redirect
from .models import Question

def quiz_view(request):
    # Initialize session data
    if 'answered_questions' not in request.session:
        request.session['answered_questions'] = []

    # Check if user has answered 2 questions
    if len(request.session['answered_questions']) >= 2:
        return redirect('result_view')  # Redirect to the result page

    # Exclude already answered questions
    answered_questions = request.session['answered_questions']
    remaining_questions = Question.objects.exclude(id__in=answered_questions)

    # Pick a random question
    question = random.choice(remaining_questions) if remaining_questions.exists() else None

    # Handle form submission
    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        if user_answer and question.correct_answer == user_answer:
            request.session['score'] += 1  # Increment score for correct answer
        request.session['answered_questions'].append(question.id)  # Mark question as answered
        request.session.modified = True  # Save session data
        return redirect('quiz_view')  # Redirect to the next question

    return render(request, 'quiz/question.html', {'question': question})
from django.utils.timezone import localtime

@login_required
def leaderboard(request):
    results = QuizResult.objects.all().order_by('-date_time')  # Fetch scores in descending order of date
    return render(request, 'quiz/leaderboard.html', {
        'results': results,
    })
from django.utils.timezone import now
from .models import QuizResult

def quiz_result(request):
    # Save the result in the database
    QuizResult.objects.create(
        user=request.user,
        score=request.session.get('score', 0),
        date_time=now()
    )

    # Clear session data
    score = request.session.get('score', 0)
    request.session.flush()

    return render(request, 'quiz/result.html', {'score': score})


# views.py
# views.py
from random import sample

from random import sample

import random
from django.shortcuts import render, redirect
from .models import Question

import random
from django.shortcuts import render, redirect
from .models import Question

import random
from django.shortcuts import render, redirect
from .models import Question

import ast

def question_view(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return redirect('quiz:start')

    # Get the removed choices and lifeline used from session
    removed_choices = request.session.get('removed_choices', [])
    lifeline_used = request.session.get('lifeline_used', False)

    # If the form is submitted (answer or 50:50 request)
    if request.method == 'POST':
        # Check if 50:50 button is clicked
        if 'use_50_50' in request.POST and not lifeline_used:
            # Mark the lifeline as used
            request.session['lifeline_used'] = True

            # Remove two incorrect choices randomly
            correct_choice = question.correct_choice
            incorrect_choices = [1, 2, 3, 4]
            incorrect_choices.remove(correct_choice)

            # Randomly select 2 incorrect answers to remove
            removed_choices = random.sample(incorrect_choices, 2)

            # Save the removed choices in session
            request.session['removed_choices'] = removed_choices

            # Don't redirect, just re-render with updated choices
            return render(request, 'quiz/question.html', {
                'question': question,
                'removed_choices': removed_choices,
                'lifeline_used': True  # Flag indicating lifeline is used
            })

        # Handle the user's answer selection (submit answer)
        user_choice = request.POST.get('choice')

        # Calculate score (optional, for later use)
        score = 1 if int(user_choice) == question.correct_choice else 0
        request.session['score'] = request.session.get('score', 0) + score

        # Get the list of remaining questions from session
        question_ids = request.session.get('question_ids', [])

        # Remove the current question from the list
        question_ids.remove(question.id)

        # If there are remaining questions, go to the next one
        if question_ids:
            next_question_id = question_ids[0]  # Get next question from list
            return redirect('quiz:question', question_id=next_question_id)
        else:
            # If no more questions, go to result page
            return redirect('quiz:result')

    return render(request, 'quiz/question.html', {
        'question': question,
        'removed_choices': None,
        'lifeline_used': lifeline_used
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import QuizResult, Question
import random

# @login_required  # Ensures the user is logged in
@login_required
def result_view(request):
    # Retrieve the user's session score
    score = request.session.get('score', 0)

    # Create and save the QuizResult
    QuizResult.objects.create(
        user=request.user,
        score=score,
    )

    # Reset the session score

    return render(request, 'quiz/result.html', {'score': score})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question
import openpyxl
from django.contrib.admin.views.decorators import staff_member_required



@staff_member_required
def upload_excel(request):
    if request.method == "POST" and request.FILES['file']:
        excel_file = request.FILES['file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            question_text, choice_1, choice_2, choice_3, choice_4, correct_choice, category, difficulty = row
            Question.objects.create(
                question_text=question_text,
                choice_1=choice_1,
                choice_2=choice_2,
                choice_3=choice_3,
                choice_4=choice_4,
                correct_choice=int(correct_choice),
                category=category,
                difficulty=difficulty,
            )

        messages.success(request, "Questions uploaded successfully!")
        return redirect('quiz:upload_excel')

    return render(request, 'quiz/upload_excel.html')

