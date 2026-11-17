"""Builds the GitHub Pages site from the two game files one folder up.

Run with: python3 build.py
The source files are written for Claude artifacts, which add the page skeleton themselves,
so this wraps each one in a full page with phone and home-screen settings.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent

GAMES = [
    # source file, page, home-screen name, manifest file
    ('note-walker-marathon.html', 'index.html', 'Note Walker Marathon', 'manifest.webmanifest'),
    ('note-walker.html', 'levels.html', 'Note Walker Levels', 'manifest-levels.webmanifest'),
]

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#E6EAF3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1121" media="(prefers-color-scheme: dark)">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="{title}">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="manifest" href="{manifest}">
<style>:root{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}*,*::before,*::after{{box-sizing:inherit}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
'''

for source, page, title, manifest in GAMES:
    s = (SRC / source).read_text()
    split = s.index('<main class="wrap">')          # everything before it is title, fonts and styles
    html = HEAD.format(title=title, manifest=manifest) + s[:split] + '</head>\n<body>\n' + s[split:] + '\n</body>\n</html>\n'
    (HERE / page).write_text(html)
    (HERE / manifest).write_text(json.dumps({
        'name': title,
        'short_name': 'Note Walker' if page == 'index.html' else 'NW Levels',
        'start_url': f'./{page}' if page != 'index.html' else './',
        'scope': './',
        'display': 'standalone',
        'background_color': '#E6EAF3',
        'theme_color': '#E6EAF3',
        'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
            {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'},
        ],
    }, indent=2) + '\n')
    print(page, manifest)
