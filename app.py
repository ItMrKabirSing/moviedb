#Copyright @ISmartCoder
#Updates Channel: t.me/TheSmartDev

from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import json
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

TMDB_SEARCH_URL = "https://www.themoviedb.org/search?query={}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_tmdb_data(query):
    start_time = time.time()
    search_url = TMDB_SEARCH_URL.format(query.replace(" ", "+"))
    app.logger.debug(f"Scraping URL: {search_url}")
    
    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find movie results container
        movie_results = soup.find("div", class_="search_results movie")
        results = []
        
        if movie_results:
            # Find all movie cards
            cards = movie_results.find_all("div", class_="card v4 tight")
            app.logger.debug(f"Found {len(cards)} movie cards")
            
            for card in cards:
                # Extract poster
                poster = card.find("img", class_="poster")
                poster_url = poster.get("src") if poster and "https://media.themoviedb.org" in poster.get("src", "") else "N/A"
                
                # Extract title
                title_elem = card.find("h2")
                title = title_elem.text.strip() if title_elem else "N/A"
                
                # Extract release year
                release_elem = card.find("span", class_="release_date")
                release_year = release_elem.text.strip() if release_elem else "N/A"
                
                # Extract rating (not visible in provided HTML, try to find or set to N/A)
                rating_elem = card.find("div", class_="user_score")
                rating = rating_elem.text.strip() if rating_elem else "N/A"
                
                # Extract overview
                overview_elem = card.find("div", class_="overview")
                overview = overview_elem.find("p").text.strip() if overview_elem and overview_elem.find("p") else "N/A"
                
                results.append({
                    "poster_url": poster_url,
                    "title": title,
                    "release_year": release_year,
                    "rating": rating,
                    "overview": overview
                })
        
        # Structure response
        result = {
            "movies": results,  # Include all results
            "total_results": len(results)
        }
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        time_taken = f"{end_time - start_time:.3f} seconds"
        
        response = {
            "status": "success",
            "health": "All systems go! 🚀",
            "ping": "Pong! 🏓",
            "latency": f"{latency_ms:.2f} ms",
            "time_taken": time_taken,
            "developer": "@ISmartCoder",
            "data": result
        }
        
        app.logger.debug(f"Scraped {len(results)} movies: {json.dumps(result, indent=2)}")
        return response
    
    except requests.RequestException as e:
        app.logger.error(f"Request error: {e}")
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        time_taken = f"{end_time - start_time:.3f} seconds"
        return {
            "status": "error",
            "health": "Something's off, but we're still kickin'! 😎",
            "ping": "Pong! 🏓",
            "latency": f"{latency_ms:.2f} ms",
            "time_taken": time_taken,
            "developer": "@ISmartCoder",
            "data": {"movies": [], "total_results": 0},
            "error": str(e)
        }
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        time_taken = f"{end_time - start_time:.3f} seconds"
        return {
            "status": "error",
            "health": "Something's off, but we're still kickin'! 😎",
            "ping": "Pong! 🏓",
            "latency": f"{latency_ms:.2f} ms",
            "time_taken": time_taken,
            "developer": "@ISmartCoder",
            "data": {"movies": [], "total_results": 0},
            "error": str(e)
        }

@app.route("/", methods=["GET"])
def status():
    return render_template("status.html")

@app.route("/api", methods=["GET"])
def api():
    query = request.args.get("query")
    if not query:
        start_time = time.time()
        latency_ms = (time.time() - start_time) * 1000
        return jsonify({
            "status": "error",
            "health": "All systems go, but I need a query! 😜",
            "ping": "Pong! 🏓",
            "latency": f"{latency_ms:.2f} ms",
            "time_taken": f"{(time.time() - start_time):.3f} seconds",
            "developer": "@ISmartCoder",
            "error": "Yo, I need a movie name to chase down! Pass a 'query' parameter."
        }), 400
    
    result = scrape_tmdb_data(query)
    return jsonify(result)

def interactive_mode():
    print("🎥 ISmartCoder Updates Channel Presents: The Movie Data Hunt! 😎")
    print("Powered by t.me/TheSmartDev, I’m here to snag the slickest movie info for ya! 🕵️‍♂️")
    query = input("So, what movie’s sparking your vibe today? (e.g., KGF, Kalki) 👉 ")
    
    if not query.strip():
        print("C’mon, don’t leave me in the dark! Drop a movie name, and let’s roll! 😜")
        return
    
    print(f"\n🔍 ISmartCoder’s diving in, searching for '{query}'... Hold up! 🚀")
    result = scrape_tmdb_data(query)
    
    print("\n🎉 Bam! Feast your eyes on this epic haul from @ISmartCoder:")
    print(json.dumps(result, indent=2))
    print("\nWant more? Run me again or hit the API at http://localhost:5000/api?query=<movie_name>! 😎")
    print("Keep it locked on ISmartCoder Updates Channel for more coding fire! 🧑‍💻")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        print("🌟 ISmartCoder’s TMDB Movie Data API is LIVE! Hit it at http://localhost:5000/api?query=<movie_name>")
        print("Brought to you by t.me/TheSmartDev & ISmartCoder Updates Channel! 🎬")
        print("Status page available at http://localhost:5000/")
        app.run(debug=True, host="0.0.0.0", port=5000)