from django.urls import path


from . import views
app_name = 'quiz'  # Define the app namespace here

urlpatterns = [
    path('', views.start_quiz, name='start'),  # Add a route for the start of the quiz
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('result/', views.result_view, name='result'),  # Make sure this URL pattern is added
    path('question/<int:question_id>/', views.question_view, name='question'),

    path('excel/', views.upload_excel, name='upload_excel'),  # New URL

    path('', views.start_quiz, name='start_quiz'),  # The start quiz view



]
