from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def web_search(query):
    search_url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = soup.select(".result__title a")
    if results:
        return results[0].get_text() + " - " + "https://duckduckgo.com" + results[0]['href']
    else:
        return "No results found."

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if "search" in user_message.lower():
        search_query = user_message.replace("search", "").strip()
        bot_response = web_search(search_query)
    else:
        bot_response = f"You said: {user_message} (I'm still learning!)"
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    @app.route("/")
    def home():
        return "Chatbot API is running!"

    app.run(host="0.0.0.0", port=5000)
