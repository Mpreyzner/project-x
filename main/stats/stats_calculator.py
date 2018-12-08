from nltk.tokenize import word_tokenize
from collections import Counter
from string import punctuation
import json
from .models import AuthorStats, TotalStats


class StatsCalculator:

    def recalculate(self, post):
        print('recalculate started for post:' + post.title)
        if post.language != 'pl':
            return

        word_tokens = word_tokenize(post.content)
        filtered_content = self.filter_out_stop_words(word_tokens)
        words_from_post_counter = Counter(filtered_content)

        self.update_author_stats(post.author, words_from_post_counter)
        self.update_total_stats(words_from_post_counter)

    def filter_out_stop_words(self, word_tokens):
        # stop words from https://github.com/stopwords-iso/stopwords-pl + 'ze'
        stop_words = {'ach', 'aj', 'albo', 'bardzo', 'bez', 'bo', 'być', 'ci', 'cię', 'ciebie', 'co', 'czy', 'daleko',
                      'dla', 'dlaczego', 'dlatego', 'do', 'dobrze', 'dokąd', 'dość', 'dużo', 'dwa', 'dwaj', 'dwie',
                      'dwoje', 'dziś', 'dzisiaj', 'gdyby', 'gdzie', 'go', 'ich', 'ile', 'im', 'inny', 'ja', 'ją', 'jak',
                      'jakby', 'jaki', 'je', 'jeden', 'jedna', 'jedno', 'jego', 'jej', 'jemu', 'jeśli', 'jest',
                      'jestem', 'jeżeli', 'już', 'każdy', 'kiedy', 'kierunku', 'kto', 'ku', 'lub', 'ma', 'mają', 'mam',
                      'mi', 'mną', 'mnie', 'moi', 'mój', 'moja', 'moje', 'może', 'mu', 'my', 'na', 'nam', 'nami', 'nas',
                      'nasi', 'nasz', 'nasza', 'nasze', 'natychmiast', 'nią', 'nic', 'nich', 'nie', 'niego', 'niej',
                      'niemu', 'nigdy', 'nim', 'nimi', 'niż', 'obok', 'od', 'około', 'on', 'ona', 'one', 'oni', 'ono',
                      'owszem', 'po', 'pod', 'ponieważ', 'przed', 'przedtem', 'są', 'sam', 'sama', 'się', 'skąd', 'tak',
                      'taki', 'tam', 'ten', 'to', 'tobą', 'tobie', 'tu', 'tutaj', 'twoi', 'twój', 'twoja', 'twoje',
                      'ty', 'wam', 'wami', 'was', 'wasi', 'wasz', 'wasza', 'wasze', 'we', 'więc', 'wszystko', 'wtedy',
                      'wy', 'żaden', 'zawsze', 'że', 'a', 'aby', 'acz', 'aczkolwiek', 'ale', 'ależ', 'aż', 'bardziej',
                      'bowiem', 'by', 'byli', 'bynajmniej', 'był', 'była', 'było', 'były', 'będzie', 'będą', 'cali',
                      'cała', 'cały', 'cokolwiek', 'coś', 'czasami', 'czasem', 'czemu', 'czyli', 'gdy', 'gdyż',
                      'gdziekolwiek', 'gdzieś', 'i', 'inna', 'inne', 'innych', 'iż', 'jakaś', 'jakichś', 'jakie',
                      'jakiś', 'jakiż', 'jakkolwiek', 'jako', 'jakoś', 'jednak', 'jednakże', 'jeszcze', 'kilka', 'kimś',
                      'ktokolwiek', 'ktoś', 'która', 'które', 'którego', 'której', 'który', 'których', 'którym',
                      'którzy', 'lat', 'lecz', 'mimo', 'między', 'mogą', 'moim', 'możliwe', 'można', 'musi', 'nad',
                      'naszego', 'naszych', 'natomiast', 'nawet', 'no', 'o', 'oraz', 'pan', 'pana', 'pani', 'podczas',
                      'pomimo', 'ponad', 'powinien', 'powinna', 'powinni', 'powinno', 'poza', 'prawie', 'przecież',
                      'przede', 'przez', 'przy', 'roku', 'również', 'sobie', 'sobą', 'sposób', 'swoje', 'ta', 'taka',
                      'takie', 'także', 'te', 'tego', 'tej', 'teraz', 'też', 'totobą', 'toteż', 'trzeba', 'twoim',
                      'twym', 'tych', 'tylko', 'tym', 'u', 'w', 'według', 'wiele', 'wielu', 'więcej', 'wszyscy',
                      'wszystkich', 'wszystkie', 'wszystkim', 'właśnie', 'z', 'za', 'zapewne', 'zeznowu', 'znów',
                      'został', 'żadna', 'żadne', 'żadnych', 'żeby', 'ze'}
        stop_words.update(list(punctuation))
        filtered_content = [w for w in word_tokens if w.lower() not in stop_words and len(w) > 1 and w.isalpha()]
        return filtered_content

    def update_total_stats(self, words_from_post_counter):
        # todo move to model
        total_stats = self.get_total_stats()
        total_stats_counter = Counter(json.loads(total_stats.word_counts))
        total_stats_counter.update(words_from_post_counter)
        total_stats.word_counts = json.dumps(total_stats_counter)
        total_stats.save()

    def get_total_stats(self):
        stats = TotalStats.objects.all().first()
        if not stats:
            stats = TotalStats(word_counts="{}")
            stats.save()
            return stats
        return stats

    def update_author_stats(self, author, words_from_post_counter):
        # todo move to model
        author_stats = self.get_author_stats(author)
        updated_author_counter = Counter(json.loads(author_stats.word_counts))
        updated_author_counter.update(words_from_post_counter)
        author_stats.word_counts = json.dumps(updated_author_counter)
        author_stats.save()

    def get_author_stats(self, author):
        stats_exists = AuthorStats.objects.filter(author=author).exists()
        if stats_exists:
            return AuthorStats.objects.get(author=author)
        stats = AuthorStats(author=author, word_counts="{}")
        stats.save()
        return stats
