#import newspaper
from newspaper import Article

url = 'http://www.lefigaro.fr/actualite-france/2019/02/18/01016-20190218ARTFIG00253-l-ecriture-inclusive-face-au-conseil-d-etat.php'
article = Article(url)
article.download()

article.parse()

print(article.text)