import nltk
from newspaper import Article

url= "https://www.thedailystar.net/news/bangladesh/crime-justice/news/serial-muggers-terrorise-mohammadpur-3506776"
article=Article(url)

article.download()
article.parse()
nltk.download('punkt')
article.nlp()
article.title

article.top_image

#print(article.text)

print(article.summary)