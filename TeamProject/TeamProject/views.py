# render 함수는 클라이언트의 요청을 처리하여 최종 결과인 HTML 문서를 클라이언트에게 되돌려 주는 역할을 합니다.
from django.shortcuts import render

from .models import NaverNews

# Create your views here.

# def NaverNews_list(request):
#     # QueerySet는 데이터 베이스 쿼리의 결과 집합을 의미하는 객체입니다.
#     # 장고에서 QuerySet의 기본 이름은 objects입니다.
#     NaverNewss = NaverNews.objects.all()
#
#     return render(request, 'TeamProject/NaverNews_list.html',{'NaverNewsList' : NaverNewss})
# # end def movie_list

from django.core.paginator import Paginator

def NaverNews_list(request): # request는 http 요청 객체입니다.
    # 요청(request)한 mode, keyword 파라미터를 챙깁니다.
    category = request.GET.get('category', None)
    company = request.GET.get('company', None)

    if category:
        NaverNewss = NaverNews.objects.filter(nCategory=category)
    else:
        NaverNewss = NaverNews.objects.all()

    if company:
        NaverNewss = NaverNewss.objects.filter(nCompany=company)

    pageSize = 10
    paginator = Paginator(NaverNewss, pageSize)

    pageNumber = request.GET.get('page')  # 사용자가 요청한 페이지 번호
    NaverNewsList = paginator.get_page(pageNumber)
    pageCount = 10
    totalPage = paginator.num_pages

    if pageNumber == None:  # 처음 시작 되었을 때
        pageNumber = 1
        beginPage = 1
        endPage = 10

    else:  # 사용자가 Pagination의 숫자를 눌렀을 때
        print('pageNumber=' + pageNumber)  # 파라미터들은 문자열로 넘어 옵니다.
        pageNumber = int(pageNumber)  # 해당 파라미터를 정수형 숫자로 변경합니다.
        beginPage = (pageNumber - 1) // pageSize * pageSize + 1
        endPage = beginPage + pageCount - 1

        # 끝 페이지가 전체 페이지 번호 보다 큰 경우, 끝페이지를  전체 페이지로 대체합니다.
        totalPage = paginator.num_pages
        if totalPage < endPage:
            endPage = totalPage
    # end if

    has_previous = pageNumber > pageCount
    print('has_previous=' + str(has_previous))

    # 주의) 몫 연산을 위하여 //로 나누어야 합니다.
    has_next = pageNumber < (totalPage // pageCount * pageCount + 1)
    print('has_next=' + str(has_next))

    print('beginPage=' + str(beginPage))
    print('endPage=' + str(endPage))

    # Template(html 문서) 파일에서는 range()를 사용할 수 없습니다.
    # 연산이 이루어 지는 과정에 실수로 바뀌기 때문에 다시 정수로 변환해줍니다.
    page_range = range(int(beginPage), int(endPage) + 1)

    # 페이지로 넘어오는 파라미터 정보
    query_params = request.GET.copy()  # 파라미터 목록의 복사본 만들기

    # page 파라미터를 제거한 다음 쿼리 문자열을 전송하도록 합니다.
    delete_param = 'page'

    if 'page' in query_params:
        del query_params[delete_param]

    # 넘겨진 쿼리 목록의 문자열 집합을 QueryString이라고 부릅니다.
    query_params = query_params.urlencode()  # 복사본을 인코딩 문자열로 변환

    print('query_params=[' + str(query_params) + ']')


    context = {'NaverNewsList': NaverNewsList, 'beginPage': beginPage, 'endPage': endPage, 'page_range': page_range, 'has_previous': has_previous, 'has_next': has_next, 'query_params': query_params}

    return render(request, 'TeamProject/NaverNews_list.html', context)
# end def movie_pagination

def NaverNews_view(request):
    idx = request.GET.get('idx', None)
    NaverNewss = NaverNews.objects.filter(nIdx=idx)

    return render(request, 'TeamProject/NaverNews_view.html', {'NaverNews': NaverNewss})
