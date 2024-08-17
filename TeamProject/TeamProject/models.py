from django.db import models

# Create your models here.
# 모델은 장고의 테이블을 정의해주는 클래스 입니다.
class NaverNews(models.Model): # 무비가 모델을 상속받는다는 뜻
    nIdx = models.IntegerField(primary_key=True)
    nCategory = models.TextField()
    nCompany = models.TextField()
    nTitle = models.TextField()
    nContent = models.TextField()
    nLink = models.TextField()
    nImage = models.TextField()
    nviews = models.IntegerField()

    # 메타 클래스 : 기본 컬럼 이외에 모델의 설정 정보를 담고 있는 내부 클래스
    # 예를 들어 테이블 이름이나, 정렬 방식 등을 설정할 수 있습니다.
    class Meta:
        app_label = 'TeamProject'
        db_table = 'NaverNews' # 이 모델은 'NaverNews' 테이블과 연동됩니다.

    # __str__ 함수는 객체를 문자열로 표현하고자 할때 사용하는 함수입니다.
    def __str__(self):
        return self

# end class NaverNews(models.Model)