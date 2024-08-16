# # render 함수는 클라이언트의 요청을 처리하여 최종 결과인 HTML 문서를 클라이언트에게 되돌려 주는 역할을 합니다.
# from django.shortcuts import render
#
# from kmdb.models import Movie
#
# # Create your views here.
#
# def movie_list(request) :
#     # QueerySet는 데이터 베이스 쿼리의 결과 집합을 의마하는 객체입니다.
#     # 장고에서 QuerySet의 기본 이름은 objects입니다.
#     movies = Movie.objects.all()
#
#     return render(request, 'kmdb/movie_list.html',{'movieList' : movies})
# # end def movie_list
#
# # 페이징 처리를 위하여 임포트 합니다.
# from django.core.paginator import Paginator
#
# def movie_pagination(request): # request는 http 요청 객체입니다.
#     movies = Movie.objects.all()
#     paginator = Paginator(movies, 10)
#
#     page_number = request.GET.get('page')
#     movieList = paginator.get_page(page_number)
#
#     return render(request, 'kmdb/movie_pagination.html',{'movieList' : movieList})
# # end def movie_pagination