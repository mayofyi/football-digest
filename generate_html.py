#!/usr/bin/env python3
"""
Generate HTML from digest data with distinctive design
"""

import json
from datetime import datetime

def generate_html(digest_data):
    """Generate beautiful HTML from digest data"""
    
    divisions_html = ""
    
    for div_key, div_data in digest_data['divisions'].items():
        articles_html = ""
        
        for article in div_data['articles']:
            articles_html += f"""
                <li class="news-item">
                    <a href="{article['link']}" target="_blank" rel="noopener">
                        <span class="news-title">{article['title']}</span>
                        <span class="news-date">{article['published']}</span>
                    </a>
                </li>
            """
        
        highlights_html = ""
        for highlight in div_data['highlights']:
            highlights_html += f"""
                <div class="highlight-link">
                    <a href="{highlight['search_url']}" target="_blank" rel="noopener">
                        🎬 Watch {div_data['name']} Highlights
                    </a>
                </div>
            """
        
        divisions_html += f"""
        <section class="division-section">
            <h2 class="division-title">{div_data['name']}</h2>
            
            {highlights_html if highlights_html else ''}
            
            <ul class="news-list">
                {articles_html if articles_html else '<li class="no-news">No recent news</li>'}
            </ul>
        </section>
        """
    
    # Standout moments
    standout_html = ""
    for moment in digest_data.get('standout_moments', []):
        standout_html += f"""
            <li class="standout-item">
                <a href="{moment['link']}" target="_blank" rel="noopener">
                    ⚡ {moment['moment']}
                </a>
            </li>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Football Digest - Week of {digest_data['week_ending']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Righteous&family=Work+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #FF3366;
            --secondary: #0D1B2A;
            --accent: #FFD60A;
            --bg: #F8F9FA;
            --text: #1B263B;
            --border: #E0E1DD;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Work Sans', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        
        .header {{
            background: var(--secondary);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(135deg, var(--primary) 0%, transparent 50%),
                linear-gradient(45deg, var(--accent) 0%, transparent 40%);
            opacity: 0.1;
            z-index: 0;
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        h1 {{
            font-family: 'Righteous', cursive;
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            background: linear-gradient(135deg, white 0%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: slideInDown 0.6s ease-out;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            opacity: 0.8;
            font-weight: 400;
            animation: fadeIn 0.8s ease-out 0.2s both;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        .standout-section {{
            background: white;
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 3rem;
            border: 3px solid var(--primary);
            box-shadow: 0 8px 24px rgba(255, 51, 102, 0.15);
            animation: slideInUp 0.6s ease-out;
        }}
        
        .standout-title {{
            font-family: 'Righteous', cursive;
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .standout-list {{
            list-style: none;
            display: grid;
            gap: 0.75rem;
        }}
        
        .standout-item {{
            padding: 1rem;
            background: linear-gradient(135deg, #FFF5F7 0%, #FFF 100%);
            border-radius: 8px;
            border-left: 4px solid var(--primary);
            transition: all 0.3s ease;
        }}
        
        .standout-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(255, 51, 102, 0.2);
        }}
        
        .standout-item a {{
            text-decoration: none;
            color: var(--text);
            font-weight: 600;
            display: block;
        }}
        
        .division-section {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
            animation: fadeIn 0.8s ease-out;
        }}
        
        .division-section:hover {{
            border-color: var(--primary);
            box-shadow: 0 4px 20px rgba(13, 27, 42, 0.08);
        }}
        
        .division-title {{
            font-family: 'Righteous', cursive;
            font-size: 1.8rem;
            color: var(--secondary);
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid var(--accent);
            text-transform: uppercase;
        }}
        
        .highlight-link {{
            background: linear-gradient(135deg, var(--secondary) 0%, #1E3A5F 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .highlight-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(13, 27, 42, 0.3);
        }}
        
        .highlight-link a {{
            color: white;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
        }}
        
        .news-list {{
            list-style: none;
            display: grid;
            gap: 0.5rem;
        }}
        
        .news-item {{
            padding: 0.75rem;
            border-radius: 6px;
            transition: background 0.2s ease;
        }}
        
        .news-item:hover {{
            background: #F8F9FA;
        }}
        
        .news-item a {{
            text-decoration: none;
            color: var(--text);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        
        .news-title {{
            flex: 1;
            font-weight: 500;
        }}
        
        .news-date {{
            font-size: 0.875rem;
            color: #6B7280;
            white-space: nowrap;
        }}
        
        .no-news {{
            color: #9CA3AF;
            font-style: italic;
            text-align: center;
            padding: 2rem;
        }}
        
        .footer {{
            background: var(--secondary);
            color: white;
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
            
            .standout-section,
            .division-section {{
                padding: 1.5rem;
            }}
            
            .news-item a {{
                flex-direction: column;
                align-items: flex-start;
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
            <h2 class="standout-title">⚡ Standout Moments</h2>
            <ul class="standout-list">
                {standout_html if standout_html else '<li class="no-news">No standout moments this week</li>'}
            </ul>
        </section>
        
        {divisions_html}
    </div>
    
    <footer class="footer">
        <p>Generated on {digest_data['generated_date']} • Updates weekly</p>
    </footer>
</body>
</html>"""
    
    return html

def main():
    """Generate HTML from digest data"""
    # Load digest data
    with open('digest_data.json', 'r', encoding='utf-8') as f:
        digest_data = json.load(f)
    
    # Generate HTML
    html = generate_html(digest_data)
    
    # Save HTML
    output_file = 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML generated successfully: {output_file}")

if __name__ == "__main__":
    main()
