#!/usr/bin/env python3
"""
Generate HTML V3 - Real Images with SVG Fallback
Tries to load images from articles, falls back to SVG if missing
"""

import json
from datetime import datetime

def get_division_icon(div_key):
    """Return SVG icon for each division (used as fallback)"""
    icons = {
        'premier_league': '''
            <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="120" fill="#38003c"/>
                <circle cx="100" cy="60" r="35" fill="none" stroke="#00ff85" stroke-width="4"/>
                <text x="100" y="70" font-family="Arial" font-size="24" font-weight="bold" fill="#00ff85" text-anchor="middle">PL</text>
            </svg>
        ''',
        'championship': '''
            <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="120" fill="#0e4c92"/>
                <polygon points="100,25 120,75 80,75" fill="#FFD700"/>
                <text x="100" y="105" font-family="Arial" font-size="18" font-weight="bold" fill="white" text-anchor="middle">CHAMPIONSHIP</text>
            </svg>
        ''',
        'league_one': '''
            <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="120" fill="#00A859"/>
                <text x="100" y="50" font-family="Arial" font-size="48" font-weight="bold" fill="white" text-anchor="middle">L1</text>
                <text x="100" y="95" font-family="Arial" font-size="16" fill="white" text-anchor="middle">LEAGUE ONE</text>
            </svg>
        ''',
        'league_two': '''
            <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="120" fill="#006B3D"/>
                <text x="100" y="50" font-family="Arial" font-size="48" font-weight="bold" fill="white" text-anchor="middle">L2</text>
                <text x="100" y="95" font-family="Arial" font-size="16" fill="white" text-anchor="middle">LEAGUE TWO</text>
            </svg>
        ''',
        'world_cup': '''
            <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="120" fill="#FFD700"/>
                <circle cx="100" cy="60" r="30" fill="none" stroke="#000" stroke-width="3"/>
                <path d="M 85 60 L 95 50 L 105 50 L 115 60 L 105 70 L 95 70 Z" fill="#000"/>
                <text x="100" y="105" font-family="Arial" font-size="14" font-weight="bold" fill="#000" text-anchor="middle">WORLD CUP</text>
            </svg>
        '''
    }
    return icons.get(div_key, icons['premier_league'])

def generate_html_v3(digest_data):
    """Generate V3 HTML with real images + SVG fallback"""
    
    divisions_html = ""
    
    for div_key, div_data in digest_data['divisions'].items():
        cards_html = ""
        
        for i, article in enumerate(div_data['articles'][:8]):
            svg_icon = get_division_icon(div_key)
            
            # Try to get image from article (if scraper extracted it)
            article_image = article.get('image', '')
            
            cards_html += f"""
                <div class="carousel-card">
                    <div class="card-image">
                        <div class="card-svg-container svg-fallback">
                            {svg_icon}
                        </div>
                        <img src="{article_image}" 
                             alt="{article['title']}" 
                             class="card-real-image"
                             loading="lazy"
                             onerror="this.style.display='none'; this.previousElementSibling.style.display='flex';"
                             onload="this.previousElementSibling.style.display='none'; this.style.display='block';">
                        <div class="card-date">{article['published']}</div>
                    </div>
                    <div class="card-content">
                        <h3 class="card-title">{article['title']}</h3>
                        <a href="{article['link']}" target="_blank" rel="noopener" class="card-link">
                            Read Full Story →
                        </a>
                    </div>
                </div>
            """
        
        highlights_html = ""
        for highlight in div_data['highlights']:
            highlights_html = f"""
                <a href="{highlight['search_url']}" target="_blank" rel="noopener" class="watch-highlights-btn">
                    ▶ Watch {div_data['name']} Highlights
                </a>
            """
        
        divisions_html += f"""
        <section class="division-section">
            <div class="division-header">
                <h2 class="division-title">{div_data['name']}</h2>
                <div class="division-controls">
                    <button class="carousel-btn prev-btn" data-division="{div_key}">‹</button>
                    <button class="carousel-btn next-btn" data-division="{div_key}">›</button>
                </div>
            </div>
            
            {highlights_html}
            
            <div class="carousel-container" id="carousel-{div_key}">
                <div class="carousel-track">
                    {cards_html if cards_html else '<div class="no-news-card">No recent news this week</div>'}
                </div>
            </div>
        </section>
        """
    
    standout_html = ""
    for moment in digest_data.get('standout_moments', [])[:6]:
        standout_html += f"""
            <div class="standout-card">
                <span class="standout-icon">⚡</span>
                <a href="{moment['link']}" target="_blank" rel="noopener">
                    {moment['moment']}
                </a>
            </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Football Digest - Week of {digest_data['week_ending']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --pitch-green: #00A859;
            --dark-green: #006B3D;
            --black: #0A0A0A;
            --white: #FFFFFF;
            --light-gray: #F5F5F5;
            --accent-yellow: #FFD700;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Outfit', -apple-system, sans-serif;
            background: var(--black);
            color: var(--white);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 100px,
                    rgba(0, 168, 89, 0.03) 100px,
                    rgba(0, 168, 89, 0.03) 200px
                );
            pointer-events: none;
            z-index: 0;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--pitch-green) 0%, var(--dark-green) 100%);
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            border-bottom: 4px solid var(--accent-yellow);
        }}
        
        .header::before {{
            content: '⚽';
            position: absolute;
            font-size: 20rem;
            opacity: 0.05;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-15deg);
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        h1 {{
            font-family: 'Bebas Neue', cursive;
            font-size: clamp(3rem, 8vw, 6rem);
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            color: var(--white);
            text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.3);
            animation: slideInDown 0.6s ease-out;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            font-weight: 600;
            opacity: 0.95;
            animation: fadeIn 0.8s ease-out 0.2s both;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 2rem;
            position: relative;
            z-index: 1;
        }}
        
        .standout-section {{
            background: linear-gradient(135deg, var(--dark-green) 0%, var(--black) 100%);
            border-radius: 20px;
            padding: 3rem;
            margin-bottom: 4rem;
            border: 3px solid var(--pitch-green);
            box-shadow: 0 10px 40px rgba(0, 168, 89, 0.3);
            animation: slideInUp 0.6s ease-out;
        }}
        
        .standout-title {{
            font-family: 'Bebas Neue', cursive;
            font-size: 2.5rem;
            color: var(--accent-yellow);
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .standout-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .standout-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid var(--accent-yellow);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .standout-card:hover {{
            transform: translateX(8px);
            background: rgba(255, 255, 255, 0.1);
            border-left-width: 8px;
        }}
        
        .standout-icon {{
            font-size: 2rem;
            flex-shrink: 0;
        }}
        
        .standout-card a {{
            color: var(--white);
            text-decoration: none;
            font-weight: 600;
            flex: 1;
        }}
        
        .division-section {{
            margin-bottom: 4rem;
            animation: fadeIn 0.8s ease-out;
        }}
        
        .division-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }}
        
        .division-title {{
            font-family: 'Bebas Neue', cursive;
            font-size: 3rem;
            color: var(--pitch-green);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-shadow: 2px 2px 0 rgba(0, 0, 0, 0.5);
        }}
        
        .division-controls {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .carousel-btn {{
            background: var(--pitch-green);
            border: none;
            color: var(--white);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 168, 89, 0.4);
        }}
        
        .carousel-btn:hover {{
            background: var(--dark-green);
            transform: scale(1.1);
        }}
        
        .carousel-btn:active {{
            transform: scale(0.95);
        }}
        
        .watch-highlights-btn {{
            display: inline-block;
            background: var(--accent-yellow);
            color: var(--black);
            padding: 1rem 2rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.1rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
        }}
        
        .watch-highlights-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 30px rgba(255, 215, 0, 0.6);
        }}
        
        .carousel-container {{
            overflow: hidden;
            position: relative;
        }}
        
        .carousel-track {{
            display: flex;
            gap: 2rem;
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 1rem 0;
        }}
        
        .carousel-card {{
            min-width: 350px;
            background: var(--white);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .carousel-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(0, 168, 89, 0.6);
        }}
        
        .card-image {{
            position: relative;
            height: 200px;
            overflow: hidden;
            background: linear-gradient(135deg, var(--pitch-green), var(--dark-green));
        }}
        
        /* SVG Fallback */
        .card-svg-container {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 0;
            left: 0;
            transition: transform 0.3s ease;
        }}
        
        .card-svg-container svg {{
            width: 100%;
            height: 100%;
        }}
        
        /* Real Image */
        .card-real-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            transition: transform 0.3s ease;
        }}
        
        .carousel-card:hover .card-svg-container,
        .carousel-card:hover .card-real-image {{
            transform: scale(1.05);
        }}
        
        .card-date {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(0, 0, 0, 0.8);
            color: var(--white);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 700;
            backdrop-filter: blur(10px);
            z-index: 10;
        }}
        
        .card-content {{
            padding: 1.5rem;
            background: var(--white);
            color: var(--black);
        }}
        
        .card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1rem;
            line-height: 1.4;
            color: var(--black);
            min-height: 3em;
        }}
        
        .card-link {{
            color: var(--pitch-green);
            text-decoration: none;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }}
        
        .card-link:hover {{
            color: var(--dark-green);
            gap: 1rem;
        }}
        
        .no-news-card {{
            min-width: 350px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 3rem;
            text-align: center;
            color: rgba(255, 255, 255, 0.5);
            font-style: italic;
        }}
        
        .footer {{
            background: var(--black);
            border-top: 3px solid var(--pitch-green);
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }}
        
        .footer p {{
            opacity: 0.7;
            font-size: 0.9rem;
        }}
        
        @keyframes slideInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
        
        @media (max-width: 768px) {{
            .header {{
                padding: 2rem 1rem;
            }}
            
            .container {{
                padding: 2rem 1rem;
            }}
            
            .standout-section {{
                padding: 2rem;
            }}
            
            .division-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }}
            
            .carousel-card {{
                min-width: 280px;
            }}
            
            .standout-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <h1>⚽ Football Digest</h1>
            <p class="subtitle">Week ending {digest_data['week_ending']}</p>
        </div>
    </header>
    
    <div class="container">
        <section class="standout-section">
            <h2 class="standout-title">⚡ Top Moments This Week</h2>
            <div class="standout-grid">
                {standout_html if standout_html else '<div class="no-news-card">No standout moments this week</div>'}
            </div>
        </section>
        
        {divisions_html}
    </div>
    
    <footer class="footer">
        <p>Generated on {digest_data['generated_date']} • Updates weekly • Made with ⚽ and code</p>
    </footer>
    
    <script>
        // Carousel functionality
        document.querySelectorAll('.prev-btn, .next-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                const division = this.dataset.division;
                const carousel = document.getElementById(`carousel-${{division}}`);
                const track = carousel.querySelector('.carousel-track');
                const cardWidth = track.querySelector('.carousel-card, .no-news-card')?.offsetWidth || 350;
                const gap = 32;
                const scrollAmount = cardWidth + gap;
                
                const currentScroll = track.style.transform ? 
                    parseInt(track.style.transform.replace('translateX(', '').replace('px)', '')) : 0;
                
                let newScroll;
                if (this.classList.contains('next-btn')) {{
                    newScroll = currentScroll - scrollAmount;
                }} else {{
                    newScroll = currentScroll + scrollAmount;
                }}
                
                const maxScroll = -(track.scrollWidth - carousel.offsetWidth);
                newScroll = Math.max(maxScroll, Math.min(0, newScroll));
                
                track.style.transform = `translateX(${{newScroll}}px)`;
            }});
        }});
        
        // Touch/swipe support
        document.querySelectorAll('.carousel-track').forEach(track => {{
            let startX = 0;
            let currentTranslate = 0;
            let prevTranslate = 0;
            let isDragging = false;
            
            track.addEventListener('touchstart', (e) => {{
                startX = e.touches[0].clientX;
                isDragging = true;
                const transform = track.style.transform;
                prevTranslate = transform ? parseInt(transform.replace('translateX(', '').replace('px)', '')) : 0;
            }});
            
            track.addEventListener('touchmove', (e) => {{
                if (!isDragging) return;
                const currentX = e.touches[0].clientX;
                currentTranslate = prevTranslate + (currentX - startX);
                track.style.transform = `translateX(${{currentTranslate}}px)`;
            }});
            
            track.addEventListener('touchend', () => {{
                isDragging = false;
            }});
        }});
    </script>
</body>
</html>"""
    
    return html

def main():
    """Generate V3 HTML from digest data"""
    with open('digest_data.json', 'r', encoding='utf-8') as f:
        digest_data = json.load(f)
    
    html = generate_html_v3(digest_data)
    
    output_file = 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ V3 HTML generated successfully: {output_file}")
    print("🖼️  Images will load from articles when available")
    print("🎨 SVG fallback displays when images fail or missing")

if __name__ == "__main__":
    main()
