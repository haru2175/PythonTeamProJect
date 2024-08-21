"""
URL configuration for DjangoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# kmdb라는 장고의 앱에서 views 모듈을 읽어 들입니다.
from TeamProject import views  # 오류가 나더라도 무시 바람

urlpatterns = [
    path('admin/', admin.site.urls),

    # 영화 목록을 표시해주는 url
    # path('요청 할 url 패턴/', 호출 할 View 함수, name='url 패턴에 부여한 이름'),
    path('NaverNews/view', views.NaverNews_view, name='NaverNews_view'),
    path('NaverNews/', views.NaverNews_list, name='NaverNews_list'),
    path('run_naver_news/', views.run_naver_news, name='run_naver_news'),
    path('run_json_to_csv/', views.run_json_to_csv, name='run_json_to_csv'),
    path('run_csv_naver_news/', views.run_csv_naver_news, name='run_csv_naver_news'),
    path('chart/team_barChart',views.chart_view_bar, name='chart/team_barChart'),
    path('chart/team_pieChart/',views.chart_view_pie, name='chart/team_pieChart'),
    # path('NaverNews/pagination', views.NaverNews_pagination, name='NaverNews_pagination'),
]

