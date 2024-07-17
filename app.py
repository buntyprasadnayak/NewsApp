from flask import Flask, render_template, request
from newsapi import NewsApiClient

app = Flask(__name__)

# Init news api
newsapi = NewsApiClient(api_key='8b4c2691245b44be8bdd1715398b04e2')

def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    # Limit the number of sources and domains to a smaller subset
    sources = ", ".join(sources[:20])
    domains = ", ".join(domains[:20])
    return sources, domains

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        related_news = newsapi.get_everything(q=keyword,
                                              sources=sources,
                                              domains=domains,
                                              language='en',
                                              sort_by='relevancy')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        all_articles = newsapi.get_everything(q=keyword,
                                              sources=sources,
                                              domains=domains,
                                              language='en',
                                              sort_by='relevancy',
                                              page_size=no_of_articles)['articles']
        return render_template("home.html", all_articles=all_articles, keyword=keyword)
    else:
        top_headlines = newsapi.get_top_headlines(country="in", language="en")
        total_results = top_headlines['totalResults']
        if (total_results > 100):
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="in",
                                                  language="en", 
                                                  page_size=total_results)['articles']
        return render_template("home.html", all_headlines=all_headlines)

if __name__ == "__main__":
    app.run(debug=True)
