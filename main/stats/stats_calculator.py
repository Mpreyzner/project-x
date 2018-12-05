from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# catch event new post scraped
# grab content from event

# check the language if it is other than polish then ignore -> using nlkt
post_content = "This is a sample sentence, showing off the stop words filtration."

stop_words = set(stopwords.words('polish'))

word_tokens = word_tokenize(post_content)

filtered_content = [w for w in word_tokens if w not in stop_words]

counter = Counter(filtered_content)

words_with_counters = counter.most_common()
# https://stackoverflow.com/questions/20510768/count-frequency-of-words-in-a-list-and-sort-by-frequency
# add to author stats
# author_stats_counter.update(new_post_counter)
# add to general stats
# Counter(words).most_common(10)

# we will be loading shittton of data into memory sooo
# maybe consider generators/iterators instead
# c.items()                       # convert to a list of (elem, cnt) pairs

# remove stop words -> https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
