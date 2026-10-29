#!/usr/bin/env python3
"""Compose a portable review page from decided configuration and trusted HTML slots.
No dependencies. Does not overwrite an existing output directory or publish anything.
"""
import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote, urlsplit

SKILL = Path(__file__).resolve().parents[1]
ASSETS = SKILL / 'assets'
GRADIENTS = {
    'green-lavender': 'linear-gradient(95.19deg, #CCEAD6 0.8%, #ECDDF4 158.87%)',
    'peach-lavender': 'linear-gradient(96.04deg, rgba(247,227,204,.65) -17.14%, #ECDDF4 94.45%)',
}
PATHS = {
    'menu': 'M3 6h18M3 12h18M3 18h18',
    'close': 'M6 6l12 12M6 18L18 6',
    'plus': 'M12 5v14M5 12h14',
    'back': 'M19 12H5m7-7-7 7 7 7',
    'print': 'M6 9V3h12v6M6 17H3V9h18v8h-3M6 14h12v7H6z',
    'help': 'M9 8a3 3 0 1 1 4 3c-1 .5-1 1-1 3M12 17h.01',
    'external': 'M14 3h7v7M21 3L10 14M10 3H3v18h18v-7',
}

def esc(value):
    return html.escape(str(value), quote=True)

def keys(obj, allowed, name):
    if not isinstance(obj, dict):
        raise ValueError(f'{name} must be an object')
    extra = set(obj) - set(allowed)
    if extra:
        raise ValueError(f'Unknown {name} keys: {sorted(extra)}')

def choice(value, values, name):
    if value not in values:
        raise ValueError(f'{name} must be one of {", ".join(values)}')
    return value

def url(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Links need a nonempty destination')
    if re.search(r'[\x00-\x20\\]', value):
        raise ValueError('URLs must not contain whitespace, controls or backslashes')
    if urlsplit(value).scheme.lower() not in ('', 'http', 'https', 'mailto', 'tel'):
        raise ValueError('Use a relative, fragment, HTTP(S), mailto or tel URL')
    if value.startswith('//'):
        raise ValueError('Use an explicit HTTPS URL instead of a protocol-relative URL')
    return esc(value)

def icon(name):
    if name not in PATHS:
        raise ValueError(f'Unknown icon {name}; available: {", ".join(PATHS)}')
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{PATHS[name]}"/></svg>'

def item_link(item, css=''):
    keys(item, ['label', 'href', 'current'], 'navigation item')
    current = ' aria-current="page"' if item.get('current') else ''
    return f'<a class="{css}" href="{url(item["href"])}"{current}>{esc(item["label"])}</a>'

def trigger(identifier, label, css='', text=False):
    contents = f'<span>{esc(label)}</span>{icon("menu")}' if text else f'{icon("menu")}<span class="sr-only">{esc(label)}</span>'
    return f'<button type="button" class="ra-icon-button {css}" data-open-dialog="{identifier}" aria-controls="{identifier}" aria-expanded="false">{contents}</button>'

def drawer(identifier, label, content, close_at=None):
    breakpoint = f' data-close-at="{close_at}"' if close_at else ''
    return f'''<dialog id="{identifier}" class="ra-drawer" aria-labelledby="{identifier}-title"{breakpoint}>
      <div class="ra-drawer-header"><h2 id="{identifier}-title" class="font-semibold">{esc(label)}</h2>
        <button type="button" class="ra-icon-button" data-close-dialog aria-label="Sulge {esc(label.lower())}">{icon('close')}</button></div>{content}</dialog>'''

def title(config, default):
    keys(config, ['text', 'actions', 'mobile_labels', 'spacing'], 'title')
    labels = choice(config.get('mobile_labels', 'icons'), ['icons', 'visible'], 'mobile_labels')
    spacing = choice(config.get('spacing', 'normal'), ['normal', 'compact', 'collection'], 'title spacing')
    actions = []
    quiet = True
    for a in config.get('actions', []):
        keys(a, ['label', 'href', 'icon', 'style'], 'title action')
        style = choice(a.get('style', 'secondary'), ['primary', 'secondary', 'quiet', 'link'], 'action style')
        quiet &= style in ('quiet', 'link')
        glyph = icon(a['icon']) if a.get('icon') else ''
        # Never hide a label if there is no visible icon to identify the action.
        label_class = 'ra-title-label--icons' if glyph and labels == 'icons' else ''
        actions.append(f'<a class="ra-action ra-action--{style}" href="{url(a["href"])}">{glyph}<span class="{label_class}">{esc(a["label"])}</span></a>')
    action_html = f'<div class="ra-title-actions {"ra-title-actions--quiet" if quiet else ""}">{"".join(actions)}</div>' if actions else ''
    return f'<div class="ra-page-title ra-page-title--{spacing}"><h1>{esc(config.get("text", default))}</h1>{action_html}</div>'

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.ids = []
    def handle_data(self, data):
        self.text.append(data)
    def handle_starttag(self, tag, attrs):
        identifier = dict(attrs).get('id')
        if identifier is not None:
            self.ids.append(identifier)

def article_sections(content):
    parsed = TextParser(); parsed.feed(content)
    if len(parsed.ids) != len(set(parsed.ids)):
        raise ValueError('Content contains duplicate IDs')
    used = set(parsed.ids)
    sections = []
    def heading(match):
        attrs, inner = match.groups()
        p = TextParser(); p.feed(inner)
        label = ' '.join(''.join(p.text).split())
        id_match = re.search(r'\bid\s*=\s*([\"\x27])(.*?)\1', attrs, re.I)
        if id_match:
            identifier = html.unescape(id_match.group(2))
            if not identifier or re.search(r'\s', identifier):
                raise ValueError('Article heading IDs must be nonempty and contain no spaces')
        else:
            slug = re.sub(r'[^\w-]+', '-', label.lower(), flags=re.U).strip('-') or 'section'
            identifier = slug; index = 2
            while identifier in used:
                identifier = f'{slug}-{index}'; index += 1
            used.add(identifier)
            attrs += f' id="{esc(identifier)}"'
        sections.append((identifier, label))
        return f'<h2{attrs}>{inner}</h2>'
    content = re.sub(r'<h2\b([^>]*)>(.*?)</h2>', heading, content, flags=re.I | re.S)
    if not sections:
        raise ValueError('Article layout needs h2 sections; choose single for unsectioned content')
    return content, sections

def make(config, content, secondary, config_dir):
    keys(config, ['app_name', 'home_url', 'lang', 'language', 'account', 'navigation', 'footer', 'gradient', 'layout', 'title', 'breadcrumbs', 'section_navigation'], 'configuration')
    name = config.get('app_name', 'Rakendus')
    layout = config.get('layout', {})
    keys(layout, ['type', 'width', 'sticky_first'], 'layout')
    kind = choice(layout.get('type', 'single'), ['single', 'split', 'workspace', 'article'], 'layout type')
    width = choice(layout.get('width', 'full' if kind != 'single' else 'medium'), ['full', 'narrow', 'medium', 'form', 'summary'], 'width')
    if kind != 'single' and width != 'full':
        raise ValueError('Split, workspace and article own their columns and require full width')
    if kind in ('split', 'workspace') and secondary is None:
        raise ValueError('Split/workspace require --secondary HTML')
    if kind in ('single', 'article') and secondary is not None:
        raise ValueError('--secondary applies only to split/workspace')
    if layout.get('sticky_first') and kind != 'split':
        raise ValueError('sticky_first applies only to split')
    nav = config.get('navigation', {})
    keys(nav, ['mode', 'items'], 'navigation')
    items = nav.get('items', [])
    mode = choice(nav.get('mode', 'both' if items else 'none'), ['both', 'drawer', 'none'], 'navigation mode')
    if mode == 'none' and items:
        raise ValueError('Navigation items would be unreachable with mode none')
    if mode != 'none' and not items:
        raise ValueError('A menu needs real items; use mode none when there are none')
    links = ''.join(item_link(item) for item in items)
    drawers = []
    desktop = f'<nav class="ra-main-nav" aria-label="Peamenüü">{links}</nav>' if mode == 'both' else ''
    menu_trigger = ''
    if mode != 'none':
        menu_trigger = trigger('main-menu', 'Ava menüü', f'ra-menu-trigger--{mode}')
        drawers.append(drawer('main-menu', 'Menüü', f'<nav class="ra-drawer-nav" aria-label="Peamenüü">{links}</nav>', 1024 if mode == 'both' else None))
    heading = title(config.get('title', {}), name)
    if kind == 'single':
        body = f'<div class="ra-width--{width}">{heading}{content}</div>'
    elif kind == 'split':
        sticky = 'ra-sticky-first' if layout.get('sticky_first', True) else ''
        body = f'{heading}<div class="ra-split"><div><div class="{sticky}">{content}</div></div><div>{secondary}</div></div>'
    elif kind == 'workspace':
        body = f'<div class="ra-workspace"><div class="ra-workspace-panel">{content}</div><div class="ra-workspace-main">{heading}{secondary}</div></div>'
    else:
        content, sections = article_sections(content)
        toc = '<nav data-toc class="ra-toc-links" aria-label="Sisukord">' + ''.join(f'<a href="#{quote(i)}">{esc(label)}</a>' for i, label in sections) + '</nav>'
        drawers.append(drawer('contents-menu', 'Sisukord', f'<div class="ra-drawer-toc">{toc}</div>', 1024))
        section_items = config.get('section_navigation', [])
        section_links = ''.join(item_link(item) for item in section_items)
        section_aside = f'<aside class="ra-section-nav"><nav aria-label="Jaotised"><h2>Jaotised</h2>{section_links}</nav></aside>' if section_items else ''
        section_mobile = ''
        if section_items:
            section_mobile = f'<div class="ra-local-menu">{trigger("section-menu", "Jaotised", text=True)}</div>'
            drawers.append(drawer('section-menu', 'Jaotised', f'<nav class="ra-drawer-nav" aria-label="Jaotised">{section_links}</nav>', 1024))
        body = f'''<div class="ra-article-layout">{section_aside}<div class="ra-article-main">{section_mobile}
          <div class="ra-toc-phone">{trigger('contents-menu', 'Sisukord', text=True)}</div>
          <div class="ra-article-columns"><article class="ra-article-body">{heading}<div data-article class="prose ra-article-prose">{content}</div></article>
          <aside class="ra-toc-desktop"><div class="ra-toc-scroll"><h2 class="ra-toc-heading">SISUKORD</h2>{toc}</div></aside>
          <div class="ra-toc-compact"><div>{trigger('contents-menu', 'Ava sisukord')}</div></div></div></div></div>'''
    if kind != 'article' and config.get('section_navigation'):
        raise ValueError('section_navigation is an ArticleLayout option')
    gradient = config.get('gradient', 'green-lavender')
    if isinstance(gradient, dict):
        keys(gradient, ['start', 'end', 'angle'], 'gradient')
        for stop in ('start', 'end'):
            if not re.fullmatch(r'#[0-9a-fA-F]{6}', gradient[stop]):
                raise ValueError('Custom gradient colors must be six-digit hex values')
        angle = float(gradient.get('angle', 95.19))
        if not 0 <= angle <= 360:
            raise ValueError('Gradient angle must be between 0 and 360')
        gradient_css = f'linear-gradient({angle}deg, {gradient["start"]} 0%, {gradient["end"]} 100%)'
    else:
        gradient_css = GRADIENTS[choice(gradient, list(GRADIENTS), 'gradient')]
    footer_config = config.get('footer', {'variant': 'standard'})
    keys(footer_config, ['variant', 'file'], 'footer')
    footer_kind = choice(footer_config.get('variant', 'standard'), ['standard', 'custom', 'none'], 'footer variant')
    if footer_kind == 'standard':
        footer_content = (ASSETS / 'fragments/footer-standard.html').read_text()
    elif footer_kind == 'custom':
        footer_content = '<div class="py-6">' + (config_dir / footer_config['file']).read_text() + '</div>'
    footer = '' if footer_kind == 'none' else (ASSETS / 'starter/footer.html').read_text().replace('@@FOOTER_CONTENT@@', footer_content)
    if footer_kind != 'custom' and 'file' in footer_config:
        raise ValueError('footer.file requires variant custom')
    breadcrumb = ''
    if config.get('breadcrumbs'):
        crumbs = '<li aria-hidden="true">›</li>'.join(f'<li>{item_link(item)}</li>' for item in config['breadcrumbs'])
        breadcrumb = f'<nav class="ra-frame" aria-label="Asukoht"><ol class="ra-breadcrumbs">{crumbs}</ol></nav>'
    language = item_link(config['language'], 'text-sm font-medium') if config.get('language') else ''
    account = item_link(config['account'], 'ra-action ra-action--primary') if config.get('account') else ''
    values = {'LANG': esc(config.get('lang', 'et')), 'DOCUMENT_TITLE': esc(config.get('title', {}).get('text', name)), 'GRADIENT': gradient_css, 'LANGUAGE_LINK': language, 'APP_NAME': esc(name), 'HOME_URL': url(config.get('home_url', './index.html')), 'DESKTOP_NAV': desktop, 'ACCOUNT_ACTION': account, 'MENU_TRIGGER': menu_trigger, 'BREADCRUMBS': breadcrumb, 'CONTENT': body, 'FOOTER': footer, 'DRAWERS': '\n'.join(drawers)}
    template = (ASSETS / 'starter/shell.html').read_text()
    rendered = re.sub(r'@@([A-Z_]+)@@', lambda m: values[m.group(1)], template)
    parsed = TextParser(); parsed.feed(rendered)
    if len(parsed.ids) != len(set(parsed.ids)):
        raise ValueError('Generated shell and content have duplicate IDs; rename content IDs')
    return rendered

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--content', required=True, type=Path, help='Trusted local HTML slot, not an entire document')
    parser.add_argument('--secondary', type=Path, help='Second slot for split/workspace')
    parser.add_argument('--output', required=True, type=Path, help='New directory, must not already exist')
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError(f'Output already exists: {args.output}; choose a new directory')
        config = json.loads(args.config.read_text())
        content = args.content.read_text()
        secondary = args.secondary.read_text() if args.secondary else None
        result = make(config, content, secondary, args.config.resolve().parent)
        args.output.mkdir(parents=True)
        dest = args.output / 'assets'; dest.mkdir()
        for file in ['style.css', 'patterns.css', 'ra_logo.svg']:
            shutil.copy2(ASSETS / file, dest / file)
        for file in ['system.css', 'runtime.js']:
            shutil.copy2(ASSETS / 'starter' / file, dest / file)
        shutil.copytree(ASSETS / 'fonts', dest / 'fonts')
        (args.output / 'index.html').write_text(result)
        (args.output / 'design-decisions.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n')
        print(args.output.resolve() / 'index.html')
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, f'compose: {error}\n')

if __name__ == '__main__':
    main()
