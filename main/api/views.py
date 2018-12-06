from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from stats.serializers import AuthorStatsSerializer, TotalStatsSerializer
from stats.models import AuthorStats, TotalStats
from scraper.serializers import AuthorSerializer
from scraper.models import Author


class AuthorList(generics.ListAPIView):
    # todo adjust formatting
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.all()
        authors = {}
        for author in queryset.all():
            authors.update({author.tokenized_name: author.name} )
        # authors = [{author.tokenized_name: author.name} for author in queryset.all()]
        return Response(authors)


# {
#   "andrzejpiasecki": "Andrzej Piasecki",
#   "kamilchudy": "Kamil Chudy",
#   "lukaszpilatowski": "ukasz Piatowski"
# }
@api_view(http_method_names=['GET'])
def author_stats(request, author):
    #TODO make this a class
    author = Author.objects.get(tokenized_name=author)
    stats = AuthorStats.objects.get(author=author)
    return Response(stats.top_10_words)


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list('top_10_words', flat=True))
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
