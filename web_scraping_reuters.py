import requests
from bs4 import BeautifulSoup
import json

def scrape_news(url):
    try:
        # Send a GET request to the news website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content in a structured manner
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the headlines and links (modify the selectors based on the website structure)
       # headlines = []: Initializes an empty list to store the extracted headlines and their corresponding links.
        headlines = []
        for item in soup.find_all('h3'):  # Adjust the tag and class based on the site
            headline = item.get_text(strip=True)
            link = item.find('a')['href'] if item.find('a') else None

            if link and not link.startswith('http'):
                link = url + link  # Handle relative links

            headlines.append({'headline': headline, 'link': link})

        return headlines

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def save_to_json(data, filename='headlines.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    news_url = input("Enter the URL")  # Replace with the desired news site
    news_headlines = scrape_news(news_url)

    if news_headlines:
        save_to_json(news_headlines)
        print(f"Saved {len(news_headlines)} headlines to headlines.json")
    else:
        print("No headlines found.")
