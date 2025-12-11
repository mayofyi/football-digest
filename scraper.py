#!/usr/bin/env python3
"""
Football Digest Scraper - IMPROVED VERSION
Filters for football-only content and separates by division
"""

import feedparser
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict
from urllib.parse import quote_plus

class FootballDigest:
    def __init__(self):
        # Use general football feeds - we'll filter by keywords
        self.feeds = [
            'http://feeds.bbci.co.uk/sport/0/football/rss.xml',  # BBC Football (all)
            'http://www.skysports.com/rss/12040',  # Sky Sports Football
        ]
        
        # Keywords to identify each division
        self.division_keywords = {
            'premier_league': [
                'premier league', 'arsenal', 'chelsea', 'liverpool', 'manchester united',
                'manchester city', 'tottenham', 'newcastle', 'brighton', 'aston villa',
                'west ham', 'fulham', 'wolves', 'everton', 'nottingham forest',
                'brentford', 'crystal palace', 'bournemouth', 'luton', 'burnley',
                'sheffield united', 'man utd', 'man city', 'spurs'
            ],
            'championship': [
                'championship', 'leeds', 'leicester', 'ipswich', 'southampton',
                'west brom', 'norwich', 'coventry', 'middlesbrough', 'preston',
                'millwall', 'blackburn', 'cardiff', 'swansea', 'sheffield wednesday',
                'hull', 'stoke', 'qpr', 'birmingham', 'plymouth', 'bristol city',
                'watford', 'sunderland'
            ],
            'league_one': [
                'league one', 'portsmouth', 'derby', 'bolton', 'barnsley',
                'peterborough', 'wycombe', 'oxford', 'lincoln', 'stevenage',
                'reading', 'northampton', 'exeter', 'charlton', 'burton',
                'port vale', 'fleetwood', 'shrewsbury', 'cambridge', 'bristol rovers',
                'cheltenham', 'carlisle'
            ],
            'league_two': [
                'league two', 'wrexham', 'notts county', 'mansfield', 'stockport',
                'bradford', 'crewe', 'doncaster', 'grimsby', 'morecambe',
                'salford', 'swindon', 'tranmere', 'walsall', 'accrington',
                'barrow', 'colchester', 'gillingham', 'harrogate', 'newport',
                'sutton', 'crawley', 'forest green'
            ],
            'world_cup': [
                'world cup', 'fifa', 'qatar', 'euros', 'euro 2024', 'euro 2025',
                'international', 'england squad', 'wales squad', 'scotland squad'
            ]
        }
        
        # Keywords to EXCLUDE (other sports)
        self.exclude_keywords = [
            'cricket', 'rugby', 'tennis', 'golf', 'formula 1', 'f1',
            'boxing', 'ufc', 'nfl', 'nba', 'baseball', 'american football',
            'athletics', 'swimming', 'cycling', 'horse racing', 'snooker',
            'darts', 'badminton', 'table tennis', 'hockey', 'handball'
        ]
        
    def is_football_article(self, title: str, summary: str) -> bool:
        """Check if article is about football (not other sports)"""
        text = (title + ' ' + summary).lower()
        
        # Exclude other sports
        for keyword in self.exclude_keywords:
            if keyword in text:
                return False
        
        # Must contain football-related terms
        football_terms = ['football', 'fc', 'goal', 'match', 'premier', 'league', 
                         'championship', 'transfer', 'manager', 'striker', 'midfielder']
        
        return any(term in text for term in football_terms)
    
    def categorize_article(self, title: str, summary: str) -> str:
        """Determine which division an article belongs to"""
        text = (title + ' ' + summary).lower()
        
        # Check each division's keywords
        for division, keywords in self.division_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return division
        
        # Default to premier league if can't determine
        return 'premier_league'
    
    def fetch_feed(self, url: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            # Get articles from last 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in feed.entries[:50]:  # Check more entries
                try:
                    # Parse published date
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                    else:
                        pub_date = datetime.now()
                    
                    # Only include recent articles
                    if pub_date < cutoff_date:
                        continue
                    
                    title = entry.title
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    # Filter: must be football
                    if not self.is_football_article(title, summary):
                        continue
                    
                    article = {
                        'title': title,
                        'link': entry.link,
                        'published': pub_date.strftime('%Y-%m-%d'),
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                        'division': self.categorize_article(title, summary)
                    }
                    articles.append(article)
                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
            return []
    
    def fetch_youtube_highlights(self, query: str) -> List[Dict]:
        """Generate YouTube search link for highlights"""
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        
        return [{
            'title': f'{query} - Week Highlights',
            'search_url': search_url,
            'embed_id': None
        }]
    
    def categorize_standout_moments(self, articles: List[Dict]) -> List[Dict]:
        """Extract standout moments from articles"""
        standout_keywords = [
            'shock', 'upset', 'stunning', 'comeback', 'record', 'historic',
            'dramatic', 'derby', 'thriller', 'controversy', 'red card',
            'hat-trick', 'injury', 'sacked', 'appointed', 'transfer',
            'signs', 'debut', 'winner', 'equaliser', 'penalty', 'crisis'
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
        
        return standout_moments[:15]  # Top 15
    
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
        
        # Initialize divisions
        for div_key, div_name in division_names.items():
            digest['divisions'][div_key] = {
                'name': div_name,
                'articles': [],
                'highlights': self.fetch_youtube_highlights(f"{div_name} highlights this week")
            }
        
        # Fetch all articles
        all_articles = []
        for feed_url in self.feeds:
            print(f"Fetching from {feed_url}...")
            articles = self.fetch_feed(feed_url)
            all_articles.extend(articles)
        
        print(f"Found {len(all_articles)} football articles")
        
        # Sort articles into divisions
        for article in all_articles:
            division = article.pop('division')  # Remove division key from article
            if division in digest['divisions']:
                digest['divisions'][division]['articles'].append(article)
        
        # Remove duplicates and limit per division
        for div_key in digest['divisions']:
            articles = digest['divisions'][div_key]['articles']
            
            # Remove duplicates based on title
            seen_titles = set()
            unique_articles = []
            for article in articles:
                if article['title'] not in seen_titles:
                    seen_titles.add(article['title'])
                    unique_articles.append(article)
            
            # Sort by date and limit
            unique_articles.sort(key=lambda x: x['published'], reverse=True)
            digest['divisions'][div_key]['articles'] = unique_articles[:15]
            
            print(f"{digest['divisions'][div_key]['name']}: {len(unique_articles)} articles")
        
        # Add overall standout moments
        digest['standout_moments'] = self.categorize_standout_moments(all_articles)
        print(f"Standout moments: {len(digest['standout_moments'])}")
        
        return digest

def main():
    """Main execution"""
    print("=" * 60)
    print("Football Digest Generator (Improved)")
    print("=" * 60)
    
    scraper = FootballDigest()
    digest = scraper.generate_digest()
    
    # Save to JSON
    output_file = 'digest_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(digest, indent=2, fp=f)
    
    print("=" * 60)
    print(f"✅ Digest generated successfully: {output_file}")
    print(f"📊 Total divisions: {len(digest['divisions'])}")
    
    for div_key, div_data in digest['divisions'].items():
        article_count = len(div_data['articles'])
        print(f"   {div_data['name']}: {article_count} articles")
    
    print(f"⚡ Standout moments: {len(digest['standout_moments'])}")
    print("=" * 60)
    
    return digest

if __name__ == "__main__":
    main()
