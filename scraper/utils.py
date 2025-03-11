import requests
from bs4 import BeautifulSoup
import openai
import google.generativeai as genai
import os

def scrape_sitemap(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if link.startswith('/'):
                link = url.rstrip('/') + link
            if link.startswith(url):
                links.add(link)

        return list(links)

    except Exception as e:
        return []

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insights(sitemap_urls, model="openai"):
    prompt = f"""
    You are analyzing a company's online presence based on its sitemap. Below is a list of all the URLs found:

    {sitemap_urls}

    Based on this structure, generate a concise business insight:

    - Company Overview:
    - Key Focus Areas:
    - Potential Opportunities:
    """

    if model == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    
    elif model == "gemini":
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        response = genai.generate_text(prompt)
        return response.text
