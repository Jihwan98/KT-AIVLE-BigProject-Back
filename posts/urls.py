from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name="posts"

router = DefaultRouter()
# 게시판 전용: 게시판 등록 (질문 업데이트), 상세 조회, 게시판 수정, 게시판 삭제
# select * from question where question_id = True
# router.register('question', views.QuestionViewSet)

# 이미지 업로드 및 진단 ,이력 조회 crud
# # select * from question where question_id = True
# router.register('questionbase', views.QuestionBaseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/questionlist', views.ListQuestionView.as_view()),
    path('api/questionlist/<int:pk>/', views.DetailQuestionView.as_view()),
    path('api/createquestion', views.CreateQuestionView.as_view()),
    path('api/questionlist/<int:pk>/delete', views.DeleteQuestionView.as_view()), # /delete 빼고 싶은데 get으로 밖에 안감
]