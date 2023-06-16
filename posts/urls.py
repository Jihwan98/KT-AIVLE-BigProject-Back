from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name="posts"

router = DefaultRouter()
# router.register('question', views.QuestionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/questionlist', views.QuestionListView.as_view()),
    path('api/picture/', views.ChatGptAnswerAPIView.as_view()),
]