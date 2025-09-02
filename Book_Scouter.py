import requests
import pycountry

def get_language_name(code):
    language = pycountry.languages.get(alpha_2=code)
    return language.name if language else "Unknown"

def get_book_details(search):

    def get_details(response):
        
        # If the input isn't an ISBN Number, redo search with input as a Book Name Query
        try:
            response["items"]
        except:
            return get_details(requests.get(f"https://www.googleapis.com/books/v1/volumes?q={search.replace(' ', '+')}").json())

        # Get useful details about the book from the response.json()

        resp = response["items"]

        titles = [book["volumeInfo"].get("title") for book in resp]
        ids = [book["id"] for book in resp]
        authors = [book["volumeInfo"].get("authors", "") for book in resp]
        publishers = [book["volumeInfo"].get("publisher", "") for book in resp]
        publish_dates = [book["volumeInfo"].get("publishedDate", "") for book in resp]
        descriptions = [book["volumeInfo"].get("description", "") for book in resp]
        categories = [book["volumeInfo"].get("categories", "") for book in resp]
        maturity_ratings = ["Intended for a Mature Audience" if book["volumeInfo"].get("maturityRating", "")=="MATURE" else "Suitable for All Ages" for book in resp]
        language = [get_language_name(book["volumeInfo"].get("language", "")) for book in resp]
        thumbnails = [f"https://books.google.com/books/publisher/content/images/frontcover/{id}?fife=w1920-h1080&source=gbs_api" for id in ids]

        # Getting Page Count from Google Books API Website in case Response doesn't have it
        page_counts = []
        for book in resp:
            page_count = book["volumeInfo"].get("pageCount", "")
            if page_count in (0, ""):
                try:
                    info_link_content = str(requests.get(book["volumeInfo"].get("infoLink", "")).content)
                    page_count = info_link_content[info_link_content[:info_link_content.find("pages")].rfind(">")+1:info_link_content.find("pages")-1]
                except:
                    page_count = ""
            page_counts.append(str(page_count))

        isbn10 = []
        isbn13 = []

        # Get ISBN Numbers from "items". If they don't exist, return ""
        for i in response["items"]:
            isbn10_value = ""
            isbn13_value = ""
            
            try:
                for j in i["volumeInfo"]["industryIdentifiers"]:
                    if j["type"] == "ISBN_10":
                        isbn10_value = j["identifier"]
                    if j["type"] == "ISBN_13":
                        isbn13_value = j["identifier"]

            except:
                pass
            
            isbn10.append(isbn10_value)
            isbn13.append(isbn13_value)

        books = []

        for i in range(len(titles)):

            books.append({"title":titles[i], "id":ids[i], "authors":", ".join(authors[i]), "publisher":publishers[i], "publish_date":publish_dates[i], "description":descriptions[i], "isbn10":isbn10[i], "isbn13":isbn13[i], "page_count":page_counts[i], "categories":", ".join(categories[i]), "maturity_rating":maturity_ratings[i], "language":language[i], "thumbnail":thumbnails[i]})

        return books

    # Get Search Results assuming input is an ISBN Number
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{search}").json()
    
    return get_details(response)

if __name__ == "__main__":

    print(get_book_details("9781974722907"))
    #print(get_book_details("one punch man"))