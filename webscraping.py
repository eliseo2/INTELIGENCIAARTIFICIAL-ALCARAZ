import snscrape.modules.twitter as sntwitter

query = '"Tecnológico de Morelia" OR "TecNM Morelia" OR "Morelia Michoacán"'

tweets = sntwitter.TwitterSearchScraper(query).get_items()

for i, tweet in enumerate(tweets):
    print(tweet.date, tweet.user.username, tweet.content)
    if i > 10:
        break
    tweets.append((tweet.user.username, tweet.content))

for user, content in tweets:
    print(f"Usuario: {user}")
    print(f"Texto: {content}\n")

print(f"Total de tweets recopilados: {len(tweets)}")
