import requests
from bs4 import BeautifulSoup

def scrape_medlineplus(base_url, num_pages=10):
    articles = []
    for i in range(1, num_pages + 1):
        url = f"{base_url}/page{i}.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        
        for article in soup.find_all('div', class_='search-results'):
            title = article.find('a').get_text(strip=True)
            content = article.find('p').get_text(strip=True)
            articles.append({'title': title, 'content': content})
    return articles

base_url = "https://medlineplus.gov/all_health_topics.html"
articles = scrape_medlineplus(base_url, num_pages=2)

print(f"Number of articles scraped: {len(articles)}")
import chromadb
from chromadb.utils import embedding_functions

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="db/")
collection = chroma_client.get_or_create_collection(name="medlineplus_articles", embedding_function=sentence_transformer_ef)

docs = [article['content'] for article in articles]
ids = [str(i) for i in range(len(articles))]

collection.add(documents=docs, ids=ids)
import chromadb
from chromadb.utils import embedding_functions

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="db/")
collection = chroma_client.get_or_create_collection(name="medlineplus_articles", embedding_function=sentence_transformer_ef)

docs = [article['content'] for article in articles]
ids = [str(i) for i in range(len(articles))]

collection.add(documents=docs, ids=ids)
