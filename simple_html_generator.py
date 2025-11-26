#!/usr/bin/env python3
"""
Simple script to convert Aronia Travel Admin Guide to HTML
"""

def create_html_guide():
    """Convert markdown guide to HTML"""
    
    # Read the markdown file
    try:
        with open("Aronia_Travel_Admin_Guide.md", 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        print("✅ Markdown file read successfully")
    except FileNotFoundError:
        print("❌ Aronia_Travel_Admin_Guide.md not found")
        return False
    
    # Simple markdown to HTML conversion (basic)
    html_content = markdown_content
    
    # Convert basic markdown elements
    html_content = html_content.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
    html_content = html_content.replace('## ', '<h2>').replace('\n', '</h2>\n')
    html_content = html_content.replace('### ', '<h3>').replace('\n', '</h3>\n')
    html_content = html_content.replace('#### ', '<h4>').replace('\n', '</h4>\n')
    
    # Convert bold and italic
    import re
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # Convert lists
    lines = html_content.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    html_content = '\n'.join(result_lines)
    
    # Convert paragraphs
    html_content = re.sub(r'\n\n([^<\n].*?)\n\n', r'\n\n<p>\1</p>\n\n', html_content, flags=re.DOTALL)
    
    # Create professional HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aronia Travel Admin Guide</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: white;
            }}
            
            h1 {{
                color: #2c5aa0;
                border-bottom: 3px solid #2c5aa0;
                padding-bottom: 10px;
                font-size: 2.5em;
                text-align: center;
                margin-bottom: 30px;
            }}
            
            h2 {{
                color: #2c5aa0;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 5px;
                margin-top: 40px;
                margin-bottom: 20px;
                font-size: 1.8em;
            }}
            
            h3 {{
                color: #4a4a4a;
                margin-top: 30px;
                margin-bottom: 15px;
                font-size: 1.4em;
            }}
            
            h4 {{
                color: #666;
                margin-top: 25px;
                margin-bottom: 10px;
                font-size: 1.2em;
            }}
            
            p {{
                margin-bottom: 15px;
                text-align: justify;
            }}
            
            ul, ol {{
                margin-bottom: 15px;
                padding-left: 30px;
            }}
            
            li {{
                margin-bottom: 8px;
            }}
            
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            
            pre {{
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                overflow-x: auto;
                margin-bottom: 20px;
            }}
            
            blockquote {{
                border-left: 4px solid #2c5aa0;
                margin: 20px 0;
                padding: 10px 20px;
                background-color: #f9f9f9;
                font-style: italic;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            
            th {{
                background-color: #2c5aa0;
                color: white;
                font-weight: bold;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            .highlight {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
            }}
            
            .warning {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
            }}
            
            .success {{
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
            }}
            
            .page-break {{
                page-break-before: always;
            }}
            
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            
            @media print {{
                body {{
                    font-size: 12pt;
                    line-height: 1.4;
                }}
                
                h1 {{
                    font-size: 24pt;
                }}
                
                h2 {{
                    font-size: 18pt;
                }}
                
                h3 {{
                    font-size: 14pt;
                }}
                
                .page-break {{
                    page-break-before: always;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏛️ Aronia Travel Admin Guide</h1>
            <p style="text-align: center; font-size: 1.2em; color: #666; margin-bottom: 40px;">
                <strong>Creating Tour Packages and Day Trips</strong><br>
                <em>Complete Administrator Manual</em>
            </p>
        </div>
        
        {html_content}
        
        <div class="footer">
            <p><strong>© 2025 Aronia Travel</strong> | All rights reserved</p>
            <p>For technical support: support@aroniatravel.com | +254 758 355 325</p>
        </div>
    </body>
    </html>
    """
    
    # Save HTML file
    try:
        with open("Aronia_Travel_Admin_Guide.html", 'w', encoding='utf-8') as f:
            f.write(html_template)
        print("✅ HTML file created: Aronia_Travel_Admin_Guide.html")
        print("📄 To create PDF:")
        print("   1. Open the HTML file in a browser")
        print("   2. Use Print > Save as PDF")
        print("   3. Choose 'Save as PDF' in the print dialog")
        return True
    except Exception as e:
        print(f"❌ Error creating HTML file: {e}")
        return False

if __name__ == "__main__":
    create_html_guide()
