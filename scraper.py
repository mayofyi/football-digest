#!/usr/bin/env python3
"""
Football Digest Scraper - V4 with Image Extraction
Extracts images from RSS feeds when available
"""

import feedparser
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict
from urllib.parse import quote_plus
import re

class FootballDigest:
    def __init__(self):
        self.feeds = [
            'http://feeds.bbci.co.uk/sport/0/football/rss.xml',
            'http://www.skysports.com/rss/12040',
        ]
        
        self.division_keywords = {
            'premier_league': [
                'premier league', 'arsenal', 'chelsea', 'liverpool', 'manchester united',
                'manchester city', 'man utd', 'man city', 'tottenham', 'spurs', 'newcastle',
                'brighton', 'aston villa', 'west ham', 'fulham', 'wolves', 'everton',
                'nottingham forest', 'brentford', 'crystal palace', 'bournemouth'
            ],
            'championship': [
                'championship', 'leeds', 'leicester', 'ipswich', 'southampton',
                'west brom', 'norwich', 'coventry', 'middlesbrough', 'sheffield wednesday',
                'sunderland', 'burnley', 'luton'
            ],
            'league_one': [
                'league one', 'portsmouth', 'derby', 'bolton', 'barnsley',
                'peterborough', 'oxford', 'charlton', 'burton'
            ],
            'league_two': [
                'league two', 'wrexham', 'notts county', 'mansfield', 'stockport',
                'bradford', 'crewe', 'doncaster', 'tranmere'
            ],
            'world_cup': [
                'world cup', 'fifa', 'international', 'england squad', 'wales squad',
                'scotland squad', 'euros', 'euro 20'
            ]
        }
        
        self.exclude_keywords = [
            'cricket', 'rugby', 'tennis', 'golf', 'formula 1', 'f1',
            'boxing', 'ufc', 'nfl', 'nba', 'baseball'
        ]
        
    def extract_image_from_entry(self, entry) -> str:
        """Extract image URL from RSS entry"""
        try:
            # Try different RSS image fields
            # Method 1: media:thumbnail
            if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                return entry.media_thumbnail[0].get('url', '')
            
            # Method 2: media:content
            if hasattr(entry, 'media_content') and entry.media_content:
                return entry.media_content[0].get('url', '')
            
            # Method 3: enclosures
            if hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if 'image' in enclosure.get('type', ''):
                        return enclosure.get('href', '')
            
            # Method 4: Look in content/summary for img tags
            content = entry.get('summary', '') + entry.get('content', [{}])[0].get('value', '')
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            if img_match:
                return img_match.group(1)
            
            return ''
        except Exception as e:
            print(f"Error extracting image: {e}")
            return ''
    
    def is_football_article(self, title: str, summary: str) -> bool:
        """Check if article is about football"""
        try:
            text = (title + ' ' + summary).lower()
            
            for keyword in self.exclude_keywords:
                if keyword in text:
                    return False
            
            football_terms = ['football', 'fc', 'goal', 'match', 'premier', 'league', 
                             'championship', 'transfer', 'manager']
            
            return any(term in text for term in football_terms)
        except Exception as e:
            print(f"Error checking if football article: {e}")
            return False
    
    def categorize_article(self, title: str, summary: str) -> str:
        """Determine division"""
        try:
            text = (title + ' ' + summary).lower()
            
            for division, keywords in self.division_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        return division
            
            return 'premier_league'
        except Exception as e:
            print(f"Error categorizing article: {e}")
            return 'premier_league'
    
    def fetch_feed(self, url: str) -> List[Dict]:
        """Fetch RSS feed with error handling and image extraction"""
        try:
            print(f"Fetching: {url}")
            feed = feedparser.parse(url)
            
            if not feed.entries:
                print(f"Warning: No entries found in {url}")
                return []
            
            articles = []
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in feed.entries[:50]:
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    else:
                        pub_date = datetime.now()
                    
                    if pub_date < cutoff_date:
                        continue
                    
                    title = entry.get('title', 'No title')
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    if not self.is_football_article(title, summary):
                        continue
                    
                    # Extract image
                    image_url = self.extract_image_from_entry(entry)
                    
                    article = {
                        'title': title,
                        'link': entry.get('link', '#'),
                        'published': pub_date.strftime('%Y-%m-%d'),
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                        'division': self.categorize_article(title, summary),
                        'image': image_url  # Add image URL
                    }
                    articles.append(article)
                    
                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue
            
            print(f"Found {len(articles)} articles from {url}")
            return articles
            
        except Exception as e:
            print(f"ERROR fetching {url}: {e}")
            return []
    
    def fetch_youtube_highlights(self, query: str) -> List[Dict]:
        """Generate YouTube link"""
        try:
            search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            return [{
                'title': f'{query} - Week Highlights',
                'search_url': search_url,
                'embed_id': None
            }]
        except Exception as e:
            print(f"Error generating YouTube link: {e}")
            return []
    
    def categorize_standout_moments(self, articles: List[Dict]) -> List[Dict]:
        """Find standout moments"""
        try:
            standout_keywords = [
                'shock', 'upset', 'stunning', 'comeback', 'record', 'historic',
                'dramatic', 'derby', 'thriller', 'hat-trick', 'sacked', 'appointed'
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
            
            return standout_moments[:15]
            
        except Exception as e:
            print(f"Error finding standout moments: {e}")
            return []
    
    def generate_digest(self) -> Dict:
        """Generate digest"""
        try:
            print("\n" + "="*60)
            print("Football Digest Generator v4 (with Images)")
            print("="*60 + "\n")
            
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
            
            for div_key, div_name in division_names.items():
                digest['divisions'][div_key] = {
                    'name': div_name,
                    'articles': [],
                    'highlights': self.fetch_youtube_highlights(f"{div_name} highlights this week")
                }
            
            all_articles = []
            for feed_url in self.feeds:
                articles = self.fetch_feed(feed_url)
                all_articles.extend(articles)
            
            print(f"\nTotal football articles found: {len(all_articles)}")
            
            # Count articles with images
            articles_with_images = sum(1 for a in all_articles if a.get('image'))
            print(f"Articles with images: {articles_with_images}")
            
            for article in all_articles:
                division = article.pop('division')
                if division in digest['divisions']:
                    digest['divisions'][division]['articles'].append(article)
            
            for div_key in digest['divisions']:
                articles = digest['divisions'][div_key]['articles']
                
                seen_titles = set()
                unique_articles = []
                for article in articles:
                    if article['title'] not in seen_titles:
                        seen_titles.add(article['title'])
                        unique_articles.append(article)
                
                unique_articles.sort(key=lambda x: x['published'], reverse=True)
                digest['divisions'][div_key]['articles'] = unique_articles[:15]
                
                count = len(unique_articles)
                images = sum(1 for a in unique_articles if a.get('image'))
                print(f"{digest['divisions'][div_key]['name']}: {count} articles ({images} with images)")
            
            digest['standout_moments'] = self.categorize_standout_moments(all_articles)
            print(f"Standout moments: {len(digest['standout_moments'])}")
            
            print("\n" + "="*60)
            return digest
            
        except Exception as e:
            print(f"\nFATAL ERROR in generate_digest: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

def main():
    """Main execution"""
    try:
        scraper = FootballDigest()
        digest = scraper.generate_digest()
        
        output_file = 'digest_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(digest, indent=2, fp=f)
        
        print(f"✅ SUCCESS! Saved to {output_file}\n")
        return 0
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
