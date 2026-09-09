# -*- coding: utf-8 -*-
"""
Phone-sized SVG route diagram: a bold thread through one day's stops, with
every stop tappable to open Baidu Maps.

Why inline SVG rather than a real map:
  - no JS library, no API key, no network needed on the day
  - Chinese tiles carry GCJ-02 / BD-09 offsets, so a route drawn from raw
    coordinates lands hundreds of metres off
  - a schematic answers "what order, and how do I get between them", which is
    what you actually need while walking; tap a stop for the real map

Sizing lesson: text inside an SVG is scaled by (rendered width / viewBox width).
A 12.5px label in a 340-wide viewBox rendered at 316px shows as 11.6px against
body text of ~14.7px — too small. MEASURE it in the browser, do not eyeball a
screenshot. The sizes below render at parity with body text.

Usage:
    svg = build_route(
        title='Monday route',
        stops=[('08:00', '留园', '¥55, pre-booked', None),
               ('10:00', '西园寺', 'free · cats', '↓ walk 10 min')],
        city='苏州',
        caption='Monday 26 Oct — one western corridor.')
"""
import urllib.parse

STEP = 58     # vertical gap between stops; below ~54 the labels collide
TOP = 30
WIDTH = 340   # matches a ~350px phone content column at roughly 1:1


def _url(addr):
    return (u'https://api.map.baidu.com/geocoder?address=%s&amp;output=html'
            % urllib.parse.quote(addr))


def build_route(title, stops, city=u'', caption=u''):
    """stops = [(time, chinese_name, detail, connector_or_None), ...]

    connector is the label for the leg ABOVE this stop, e.g. '↓ walk 10 min'
    or '↓ 6号线'. Pass None for the first stop.
    """
    height = TOP + STEP * (len(stops) - 1) + 40
    out = [u'<figure class="diagram">',
           u'<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (WIDTH, height, title),
           u'  <line class="r-line" x1="20" y1="%d" x2="20" y2="%d"/>'
           % (TOP, TOP + STEP * (len(stops) - 1))]
    for i, (t, name, detail, conn) in enumerate(stops):
        y = TOP + STEP * i
        if conn:
            out.append(u'  <text class="r-conn" x="30" y="%d">%s</text>' % (y - 20, conn))
        out.append(u'  <circle class="r-dot" cx="20" cy="%d" r="6"/>' % y)
        out.append(u'  <text class="r-num" x="20" y="%s">%d</text>' % (y + 3.5, i + 1))
        out.append(u'  <a href="%s">' % _url(city + name))
        out.append(u'    <text class="r-name" x="38" y="%d">%s</text>' % (y + 2, name))
        out.append(u'  </a>')
        out.append(u'  <text class="r-time" x="38" y="%d">%s &middot; %s</text>'
                   % (y + 18, t, detail))
    out.append(u'</svg>')
    if caption:
        out.append(u'<figcaption>%s</figcaption>' % caption)
    out.append(u'</figure>')
    return u'\n'.join(out)


# Drop this into the page's <style>. Sizes chosen to render at body-text parity.
CSS = u"""
    #content .diagram svg { display:block; width:100%; height:auto; max-width:430px;
                            margin:0 auto; overflow:visible; }
    .r-line { stroke: #d0021b; stroke-width: 4; stroke-linecap: round; }
    .r-dot  { fill: #d0021b; stroke: #fff; stroke-width: 2; }
    .r-num  { fill: #fff; font-size: 9px; font-weight: 700; text-anchor: middle; }
    .r-name { fill: #0a58ca; font-size: 15.5px; font-weight: 600; text-decoration: underline; }
    .r-time { fill: #6b6b6b; font-size: 12.5px; }
    .r-conn { fill: #8a8a8a; font-size: 11.5px; }

    @media (prefers-color-scheme: dark) {
      .r-dot  { stroke: #1c1c1e; }
      .r-name { fill: #6ea8fe; }
      .r-time { fill: #9a9a9e; }
      .r-conn { fill: #7a7a7e; }
    }
"""

# Browser check to run after rendering. In SVG, a.href is an SVGAnimatedString,
# NOT a string — use getAttribute('href') or .href.baseVal or the test lies.
BROWSER_CHECK = u"""
const svg = document.querySelector('figure.diagram svg');
const vb = svg.viewBox.baseVal, r = svg.getBoundingClientRect();
const scale = r.width / vb.width;
const body = parseFloat(getComputedStyle(document.querySelector('#content td')).fontSize);
const name = parseFloat(getComputedStyle(svg.querySelector('.r-name')).fontSize) * scale;
let overflow = [];
svg.querySelectorAll('text').forEach(t => {
  const b = t.getBBox();
  if (b.x + b.width > vb.width + 0.5) overflow.push(t.textContent);
});
({ nameOnScreenPx: name, bodyPx: body, readable: name >= body * 0.95,
   overflow, stopsTappable: svg.querySelectorAll('a').length,
   hrefsOk: [...svg.querySelectorAll('a')]
     .every(a => (a.getAttribute('href')||'').startsWith('https://api.map.baidu.com')) })
"""

if __name__ == '__main__':
    # Write rather than print: a Windows console (cp1252) cannot encode Chinese
    # and a bare print() makes a working function look broken.
    svg = build_route(
        u'Demo route',
        [(u'08:00', u'留园', u'¥55', None),
         (u'10:00', u'西园寺', u'free', u'↓ walk 10 min')],
        u'苏州', u'Demo')
    import io as _io
    _io.open('demo_route.svg.html', 'w', encoding='utf-8').write(svg)
    print('ok: %d chars, %d stops, %d links -> demo_route.svg.html'
          % (len(svg), svg.count('r-dot'), svg.count('<a href')))
