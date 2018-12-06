from rest_framework import generics
from stats.serializers import AuthorStatsSerializer, TotalStatsSerializer
from stats.models import AuthorStats, TotalStats
from scraper.serializers import AuthorSerializer
from scraper.models import Author


class AuthorList(generics.ListAPIView):
    # todo adjust formatting
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# {
#   "andrzejpiasecki": "Andrzej Piasecki",
#   "kamilchudy": "Kamil Chudy",
#   "lukaszpilatowski": "ukasz Piatowski"
# }

class AuthorStats(generics.ListAPIView):
    queryset = AuthorStats.objects.all()
    serializer_class = AuthorStatsSerializer


# {
#   "TEONITE": 500,
#   "jest": 444,
#   "super": 333,
#   "tra": 234,
#   "la": 456,
#   "lala": 678,
#   "heja": 123,
#   "ho": 4564,
#   "pa": 55,
#   "papa": 345
# }

class TotalStats(generics.ListAPIView):
    queryset = TotalStats.objects.all()
    serializer_class = TotalStatsSerializer
    #
    # {
    #     "TEONITE": 2311,
    #     "jest": 3455,
    #     "super": 4566,
    #     "tra": 2323,
    #     "la": 4545,
    #     "lala": 4545,
    #     "heja": 8979,
    #     "ho": 9090,
    #     "pa": 2323,
    #     "papa": 4545
    # }
