from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name="posts"

router = DefaultRouter()
router.register('picture', views.PictureViewSet)
router.register('question', views.QuestionViewSet)
# router.register('answer', views.AnswerViewSet)
router.register(r"question/(?P<questionid>\d+)/answer", views.AnswerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/question-list-my/', views.QuestionList.as_view()),
    path('api/picture-list-my/', views.PictureList.as_view()),
]