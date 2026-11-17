"""Builds the GitHub Pages site from the two game files one folder up.

Run with: python3 build.py
The source files are written for Claude artifacts, which add the page skeleton themselves,
so this wraps each one in a full page with phone and home-screen settings, and adds a link
back to the game menu (index.html, which is written by hand).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent

GAMES = [
    # source file, page, title on the home screen
    ('note-walker-marathon.html', 'marathon.html', 'Note Walker Marathon'),
    ('note-walker.html', 'learn.html', 'Note Walker Learn'),
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
<link rel="manifest" href="manifest.webmanifest">
<style>:root{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}*,*::before,*::after{{box-sizing:inherit}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}
.menu-link{{display:inline-block;margin-bottom:6px;font-weight:700;font-size:.85rem;color:var(--muted);text-decoration:none;border:1px solid var(--rule);border-radius:999px;padding:3px 12px;background:var(--panel)}}
.menu-link:hover{{color:var(--ink);border-color:var(--muted)}}</style>
'''
MENU_LINK = '<a class="menu-link" href="./">&lsaquo; All games</a>\n      '

for source, page, title in GAMES:
    s = (SRC / source).read_text()
    s = s.replace('<div class="brand">\n      <h1>', '<div class="brand">\n      ' + MENU_LINK + '<h1>', 1)
    assert MENU_LINK in s, f'menu link not added to {page}'
    split = s.index('<main class="wrap">')          # everything before it is title, fonts and styles
    html = HEAD.format(title=title) + s[:split] + '</head>\n<body>\n' + s[split:] + '\n</body>\n</html>\n'
    (HERE / page).write_text(html)
    print(page)

# One home-screen app for the whole site; it opens on the game menu.
(HERE / 'manifest.webmanifest').write_text(json.dumps({
    'name': 'Note Walker',
    'short_name': 'Note Walker',
    'start_url': './',
    'scope': './',
    'display': 'standalone',
    'background_color': '#0b0b0b',
    'theme_color': '#E6EAF3',
    'icons': [
        {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
        {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'},
    ],
}, indent=2) + '\n')

# The Learn game used to live at levels.html; send old links and home-screen icons to the new page.
(HERE / 'levels.html').write_text('''<!doctype html>
<meta charset="utf-8">
<title>Note Walker Learn</title>
<meta http-equiv="refresh" content="0; url=learn.html">
<link rel="canonical" href="learn.html">
<a href="learn.html">Note Walker Learn has moved here.</a>
''')
print('manifest.webmanifest levels.html (redirect)')
