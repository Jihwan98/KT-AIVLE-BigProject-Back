from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name="posts"

router = DefaultRouter()
router.register('picture', views.PictureViewSet)
router.register('question', views.QuestionViewSet)
router.register(r"question/(?P<questionid>\d+)/answer", views.AnswerViewSet) # questionid 에 딸린 댓글 목록을 조회 및 생성

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/question-list-my/', views.QuestionList.as_view()),
    path('api/picture-list-my/', views.PictureList.as_view()),
]