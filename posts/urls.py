from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name="posts"

router = DefaultRouter()
router.register('picture', views.PictureViewSet)
router.register('question', views.QuestionViewSet)
router.register('history', views.HistoryViewSet)
router.register('answer', views.AnswerViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]