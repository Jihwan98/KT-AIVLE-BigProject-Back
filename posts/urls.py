from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name="posts"

router = DefaultRouter()
router.register('question', views.QuestionViewSet) # 게시판 등록(create), 상세 조회, 게시판 수정, 게시판 삭제

# 이미지 업로드 및 진단 ,이력 조회 crud
# # select * from question where question_id = True
# router.register('questionbase', views.QuestionBaseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/questionlist', views.ListQuestionView.as_view()),
]