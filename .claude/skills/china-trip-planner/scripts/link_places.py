# -*- coding: utf-8 -*-
"""
Inline-link Chinese place names in an HTML document to Baidu Maps.

Key-free endpoint, name-based (never coordinates), overlap-safe.

Why overlap-safety matters: a naive implementation replaces a match then keeps
searching the SAME now-HTML-containing string, so a substring gets linked INSIDE
the link just created — e.g. 北外滩 linked, then 外滩 linked inside it. That is a
nested <a>, which is invalid HTML and which browsers silently restructure.

This resolves every match on the clean text first, drops overlaps, and builds
the output once.

Usage:
    from link_places import link_document
    html = link_document(html, PLACES, section_classes=('day', 'eat'))

PLACES is a list of (chinese_name, search_prefix) tuples. The prefix is city
context for disambiguation, e.g. ('拙政园', '苏州') or a metro prefix
('拙政园苏博站', '苏州地铁'). Pass '' for names that are already unique.
"""
import re
import urllib.parse

TAG = re.compile(r'<[^>]+>')


def baidu_url(name, prefix=u''):
    """Baidu's documented, key-free geocoder endpoint.

    Renders in a browser and redirects to the mobile map, which offers to open
    the app. Works for places, metro stations and station exits.

    NOTE the &amp; — a raw & in an href is parsed as an HTML entity, and
    '&region=' becomes '&reg;' + 'ion=' (®). Always escape.
    """
    return (u'https://api.map.baidu.com/geocoder?address=%s&amp;output=html'
            % urllib.parse.quote(prefix + name))


def _link_text_node(text, places, used):
    """Link the first unused occurrence of each place inside one text node."""
    hits = []
    for name, prefix in places:
        if name in used:
            continue
        i = text.find(name)
        if i < 0:
            continue
        # reject anything overlapping an already-accepted (longer) match
        if any(not (i + len(name) <= a or i >= b) for a, b, _, _ in hits):
            continue
        hits.append((i, i + len(name), name, prefix))
    if not hits:
        return text
    hits.sort()
    out, pos = [], 0
    for a, b, name, prefix in hits:
        out.append(text[pos:a])
        out.append(u'<a href="%s">%s</a>' % (baidu_url(name, prefix), name))
        used.add(name)
        pos = b
    out.append(text[pos:])
    return u''.join(out)


def link_chunk(chunk, places):
    """Link inside one chunk of HTML, never touching attributes or nested <a>."""
    parts, tags = TAG.split(chunk), TAG.findall(chunk)
    used, depth, out = set(), 0, []
    for i, text in enumerate(parts):
        out.append(_link_text_node(text, places, used) if (depth == 0 and text) else text)
        if i < len(tags):
            t = tags[i]
            if re.match(r'<a\b', t):
                depth += 1
            elif re.match(r'</a>', t):
                depth = max(0, depth - 1)
            out.append(t)
    return u''.join(out)


def link_document(html, places, section_classes=('day',)):
    """Link place names inside <section class="..."> blocks only.

    Restricting to day/food sections keeps the rest of the prose clean and
    stops the page turning into a wall of blue.
    """
    places = sorted(places, key=lambda p: -len(p[0]))   # longest first
    for cls in section_classes:
        html = re.sub(
            r'(<section class="%s">)(.*?)(</section>)' % re.escape(cls),
            lambda m: m.group(1) + link_chunk(m.group(2), places) + m.group(3),
            html, flags=re.S)
    return html


def audit(html):
    """Run after linking. All three must be clean."""
    return {
        'nested_anchors': len(re.findall(r'<a\b[^>]*>(?:(?!</a>).)*<a\b', html, re.S)),
        'unbalanced_anchors': html.count('<a ') - html.count('</a>'),
        'unescaped_ampersand_in_href': len([
            u for u in re.findall(r'href="([^"]+)"', html)
            if re.search(r'&(?!amp;|#)', u)]),
    }


if __name__ == '__main__':
    demo = u'<section class="day"><p>北外滩 then 外滩</p></section>'
    places = [(u'北外滩', u'上海'), (u'外滩', u'上海')]
    out = link_document(demo, places)
    print(audit(out))          # nested_anchors must be 0
