from django.urls import path, re_path

from learn.views import Learning, LearningById, SectionLearn, LearningSection, Categoryl, LearningByCat, AllLearn, \
    AddLearn, AddSection, AddLesson, AllLearnWeb, AddLearnWeb, AddSectionWeb, AddLessonWeb, IndexWeb, AllSectionWeb, \
    AllLessonWeb, SingleLessonWeb

urlpatterns = [
    path('cat/', Categoryl.as_view(), name='cat-learn'),
    path('', Learning.as_view(), name='learn'),
    path('<int:pk>/', LearningById.as_view(), name='learn-by-id'),
    path('learn/<int:pk>/', LearningByCat.as_view(), name='learn-by-cat'),
    path('section/<int:pk>/', SectionLearn.as_view(), name='section'),
    path('lesson/<int:pk>/', LearningSection.as_view(), name='lesson'),
    path('all/', AllLearn.as_view(), name='learn-web'),
    path('add/', AddLearn.as_view(), name='add-learn-web'),
    path('section/', AddSection.as_view(), name='add-section-web'),
    path('lesson/', AddLesson.as_view(), name='add-lesson-web'),
    path('index/', IndexWeb.as_view(), name='index-web'),
    path('all/web/', AllLearnWeb.as_view(), name='learn-web-web'),
    path('all/section/web/<int:pk>/', AllSectionWeb.as_view(), name='section-web-web'),
    path('all/lesson/web/<int:pk>/', AllLessonWeb.as_view(), name='lesson-web-web'),
    path('all/lesson/single/<int:pk>/', SingleLessonWeb.as_view(), name='lesson-single-web'),
    path('add/web/', AddLearnWeb.as_view(), name='add-learn-web-web'),
    path('section/web/<int:pk>/', AddSectionWeb.as_view(), name='add-section-web-web'),
    path('lesson/web/<int:pk>/', AddLessonWeb.as_view(), name='add-lesson-web-web'),
]
