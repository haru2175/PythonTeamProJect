from django.db import models

# Create your models here.
# 모델은 장고의 테이블을 정의해주는 클래스 입니다.
class Movie(models.Model):
    movieCd = models.TextField(primary_key=True)
    movieNm = models.TextField()
    movieNmEn = models.TextField()
    prdtYear = models.FloatField()
    openDt = models.FloatField()
    typeNm = models.TextField()
    prdtStatNm = models.TextField()
    nationAlt = models.TextField()
    genreAlt = models.TextField()
    repNationNm = models.TextField()
    repGenreNm = models.TextField()

    # 메타 클래스 : 기본 컬럼 이외에 모델의 설정 정보를 담고 있는 내부 클래스
    # 예를 들어 테이블 이름이나, 정렬 방식들을 설정할 수 있습니다.
    class Meta :
        db_table = 'movies' # 이 모델은 'movies' 테이블과 연동됩니다.

    # __str__ 함수는 객체를 문자열로 표현하고자 할 때 사용하는 함수 입니다.
    def __str__(self):
        return self.movieNm
    
# end class Movie(models.Model