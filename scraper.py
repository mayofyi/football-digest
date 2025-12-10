#!/usr/bin/env python3
"""
Football Digest Scraper
Automatically aggregates Premier League, EFL, and World Cup football news
"""

import feedparser
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from urllib.parse import quote_plus

class FootballDigest:
    def __init__(self):
        self.feeds = {
            'premier_league': [
                'https://www.bbc.com/sport/football/premier-league/rss',
                'http://www.skysports.com/rss/12040',
            ],
            'championship': [
                'https://www.bbc.com/sport/football/championship/rss',
            ],
            'league_one': [
                'https://www.bbc.com/sport/football/league-one/rss',
            ],
            'league_two': [
                'https://www.bbc.com/sport/football/league-two/rss',
            ],
            'world_cup': [
                'https://www.bbc.com/sport/football/world-cup/rss',
            ]
        }
        
    def fetch_feed(self, url: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            # Get articles from last 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in feed.entries[:20]:  # Limit to 20 most recent
                try:
                    # Parse published date
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                    else:
                        pub_date = datetime.now()
                    
                    # Only include recent articles
                    if pub_date < cutoff_date:
                        continue
                    
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': pub_date.strftime('%Y-%m-%d'),
                        'summary': entry.get('summary', '')[:200] + '...' if len(entry.get('summary', '')) > 200 else entry.get('summary', '')
                    }
                    articles.append(article)
                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
            return []
    
    def fetch_youtube_highlights(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Fetch YouTube highlights for a given query
        Note: In production, you'd use YouTube Data API with an API key
        For now, this returns a placeholder structure
        """
        # YouTube Data API would require an API key
        # Format: https://www.youtube.com/results?search_query={query}
        
        # Placeholder - in production this would use YouTube Data API
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        
        return [{
            'title': f'{query} - Week Highlights',
            'search_url': search_url,
            'embed_id': None  # Would come from API
        }]
    
    def categorize_standout_moments(self, articles: List[Dict]) -> List[str]:
        """Extract standout moments from article titles and summaries"""
        standout_keywords = [
            'shock', 'upset', 'stunning', 'comeback', 'record', 'historic',
            'dramatic', 'derby', 'thriller', 'controversy', 'red card',
            'hat-trick', 'injury', 'sacked', 'appointed', 'transfer'
        ]
        
        standout_moments = []
        
        for article in articles:
            title_lower = article['title'].lower()
            summary_lower = article.get('summary', '').lower()
            
            for keyword in standout_keywords:
                if keyword in title_lower or keyword in summary_lower:
                    standout_moments.append({
                        'moment': article['title'],
                        'link': article['link']
                    })
                    break
        
        return standout_moments[:10]  # Top 10 standout moments
    
    def generate_digest(self) -> Dict:
        """Generate complete digest for all divisions"""
        digest = {
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'week_ending': datetime.now().strftime('%B %d, %Y'),
            'divisions': {}
        }
        
        division_names = {
            'premier_league': 'Premier League',
            'championship': 'Championship',
            'league_one': 'League One',
            'league_two': 'League Two',
            'world_cup': 'World Cup'
        }
        
        all_standout_moments = []
        
        for division_key, division_name in division_names.items():
            print(f"Fetching {division_name}...")
            
            articles = []
            for feed_url in self.feeds.get(division_key, []):
                articles.extend(self.fetch_feed(feed_url))
            
            # Remove duplicates based on title
            seen_titles = set()
            unique_articles = []
            for article in articles:
                if article['title'] not in seen_titles:
                    seen_titles.add(article['title'])
                    unique_articles.append(article)
            
            # Sort by date
            unique_articles.sort(key=lambda x: x['published'], reverse=True)
            
            # Get highlights
            highlights = self.fetch_youtube_highlights(f"{division_name} highlights this week")
            
            # Collect standout moments
            all_standout_moments.extend(self.categorize_standout_moments(unique_articles[:20]))
            
            digest['divisions'][division_key] = {
                'name': division_name,
                'articles': unique_articles[:15],  # Top 15 articles
                'highlights': highlights
            }
        
        # Add overall standout moments
        digest['standout_moments'] = all_standout_moments[:15]
        
        return digest

def main():
    """Main execution"""
    print("Starting Football Digest generation...")
    
    scraper = FootballDigest()
    digest = scraper.generate_digest()
    
    # Save to JSON
    output_file = 'digest_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(digest, indent=2, fp=f)
    
    print(f"✅ Digest generated successfully: {output_file}")
    print(f"📊 Total divisions: {len(digest['divisions'])}")
    print(f"⚡ Standout moments: {len(digest['standout_moments'])}")
    
    return digest

if __name__ == "__main__":
    main()
