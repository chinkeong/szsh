---
name: china-trip-planner
description: >
  Plan a trip to mainland China and build it into a usable, verified itinerary
  document — with Chinese place names, tappable Baidu map links for every place,
  metro station and exit, day-route diagrams, a time-gated booking calendar, an
  on-the-ground payment guide, and a Chinese phrasebook for asking locals for
  help. Use whenever someone is planning travel to China (Shanghai, Suzhou,
  Beijing, Chengdu, Xi'an, anywhere on the mainland), asks to research Chinese
  attractions, hotels, trains, metro, payments or SIM/internet, wants an
  itinerary turned into a web page or HTML guide, or asks to verify a China
  travel plan someone else wrote. Trigger on "plan my trip to China", "China
  itinerary", "Shanghai/Suzhou/Beijing trip", "how do I pay in China", "12306",
  "Alipay/WeChat/Touch n Go in China", "China metro", "gaotie / high-speed rail
  booking", "add map links to my itinerary", or any request to fact-check a
  China travel document. Also use when adding Baidu/Amap deep links to place
  names in any document.
---

# China trip planner

Two things make China travel documents fail: **English-language sources are
routinely wrong or stale about China**, and **the operational layer** — booking
windows, payment rails, which QR code is which — **is where trips actually
break**, not the sightseeing.

This skill exists so that layer is never re-derived from scratch.

---

## 1. Verification discipline — read this first

**Do not trust English travel sites, aggregators or other models on China
facts.** In one real planning session, the following were all wrong in
English-language sources and only corrected by going to Chinese primary sources:

| Claim from an English/secondary source | Reality |
|---|---|
| Yu Garden "open 09:00–21:50" | Garden shuts **16:30 daily**. The evening thing is a **separate ticketed guided tour** (¥218–258) from a different gate. Booking sites merge two products into one hours string. |
| Tiger Hill has no metro | **虎丘站 opened with Suzhou Line 6 in June 2024**, ~400 m from the gate. Guides predate it. |
| Airline flies from Terminal 1 | Juneyao 吉祥航空 uses **PVG T2 / Satellite S2**. Wrong terminal = missed flight. |
| Airport Link Line reaches Hongqiao Railway Station | It terminates at **虹桥2号航站楼 — the airport**. 10–15 min walk to the railway station. |
| Airport coach is the easy option | **First PVG→Suzhou coach ~09:10.** Useless for a dawn arrival. |
| Insurer's evacuation cover RM100,000 | Insurer's **own PDF benefit table** said RM500,000–1,500,000 by tier. A 15× error. |
| Touch 'n Go cap RM5,000 | **RM20,000** single transaction in China since March 2024. |
| Line 2 needs a change at Guanglan Road | Through-running since **April 2019**. Seven years stale. |
| Crab-roe noodles 蟹黄面 are a tourist trap | A genuine autumn speciality; **late Oct is peak**. The warning inverts the advice. |
| "74 Bib Gourmand in Shanghai" | **35.** The number was invented somewhere upstream. |

**Where to verify instead**

- Government: `*.gov.cn` — city government, 人民银行, 移民局/NIA, 园林局
- Local information portals: `<city>.bendibao.com` — reliable on metro, hours, tickets
- The operator's own site: metro companies, museums, 12306, airlines
- The company's own PDF: insurance benefit tables, product brochures
- Chinese Wikipedia `zh.wikipedia.org` for station/line facts
- Search **in Chinese**. English queries surface English SEO content, which is
  where the errors live.

**Reachability:** most Chinese sites respond fine (`dianping.com`, `amap.com`,
`baike.baidu.com`, `bendibao.com`). Some hosts refuse foreign connections —
`sz-mtr.com`, `shmetro.com` did. If a host refuses, use `bendibao` or the city
government site instead. Beware rate-limiting: Baidu returns `000` to rapid
loops but `200` to spaced single requests — **do not conclude links are broken
from a burst test**.

---

## 2. The operational checklist

Work through this for any China trip. These are the things that actually go
wrong.

### Booking windows — build a dated calendar
- **Trains (12306):** window is **15 days including the purchase day** — for a
  28 Oct train, buy on **14 Oct**, not the 13th. Release is per departure
  station at a set time (e.g. 08:30).
- **12306 registration:** use the **English platform** `www.12306.cn/en` — it
  registers by **email**. The Chinese site only accepts mainland/HK/Macau/Taiwan
  mobiles. Register weeks ahead; verification can be rejected on a name or photo
  mismatch. **Trip.com is the pragmatic default** if 12306 is painful.
- **Gardens/attractions:** many are **real-name, timed-slot, online-only**.
  Suzhou's 拙政园, 狮子林, 留园 stopped selling at the gate in **April 2019**.
  Window is typically 1–7 days ahead. **Refunds are whole-order only** — so
  **book each site as a separate order** if any might be dropped.
- **Museums:** often free but mandatory booking, released N days ahead at a fixed
  hour. Where "N days" is ambiguous about whether today counts, **tell the user
  to try both mornings** rather than guessing.
- **No-show penalties** are real (booking bans). Cancel rather than skip.

### Payments — the concept that explains everything
- **收款码** = *their* code, you scan it. Foreign wallets (Touch 'n Go via
  Alipay+) work here.
- **付款码** = *your* code, they scan you. **Foreign wallets cannot generate
  one.** This is why TnG fails at **metro gates, supermarket tills and
  restaurant scan-to-order 扫码点单**, and why it can't do **DiDi**.
- **Real Alipay 支付宝 with a linked foreign card is the one that does
  everything.** 3% fee above ¥200, nothing at or below.
- **WeChat balance 零钱 cannot be topped up with a foreign card** (needs a
  mainland bank account). Install it for **messaging**, not payment.
- **Cash is legally guaranteed.** A PBOC/NDRC regulation effective
  **1 Feb 2026** bars refusing cash 不得拒收现金 and requires a manual cash
  channel. Fines ¥1,000–50,000. So the worst case is always "pay cash".
- **云闪付 (UnionPay app)** takes foreign cards and has a 旅行通卡 top-up. Matters
  where gates read UnionPay but not Visa/Mastercard.
- Tell the user to **enable "Pay Abroad"/cross-border in their home wallet
  before flying**, and to set up payment on **both phones**.

### Internet
- **Roaming ≠ local SIM.** Home-routed roaming bypasses the firewall — WhatsApp
  and Google keep working. A **China-local SIM/eSIM puts them inside it**. These
  are opposite outcomes; never present them as alternatives.
- Google Maps is unusable even with a VPN. Use **Amap 高德地图** or **Baidu
  百度地图**; Apple Maps works natively on iPhone.
- Install and test everything **before departure** — app stores and VPN sites are
  unreachable on arrival.

### Physical
- **Plug types differ.** Malaysia/UK/Singapore/HK use Type G; China uses A/I.
  Voltage is compatible, so it's an adapter not a converter — but a dead phone
  means no payment, no metro, no map.
- Power banks need a visible **3C** mark for Chinese security.
- Squat toilets are the default; carry tissues. No tipping. Tap water not
  drinkable.

### Medical and insurance
- Most travel insurance **reimburses** — it does not pay the hospital. Cash-flow
  problem first, insurance problem second.
- Ask for a **Guarantee of Payment (GOP)** from the 24-hour assistance line for
  large bills.
- Go to the **国际医疗部 / 特需门诊**, not the general **急诊**.
- **Claims fail on paperwork.** Must collect: **发票** (official tax receipt —
  a card slip or Alipay screenshot is *not* one), **费用明细单**, **病历/出院小结**,
  **诊断证明**, test reports, **支付凭证**. Teach the phrase **我要发票**.
- Check the policy's **evacuation limit** specifically — comparison sites show
  medical expenses and omit evacuation, and they differ by an order of magnitude.

---

## 3. Build recipes

### Baidu map links — key-free, name-based
The endpoint that needs **no API key** and renders in a browser:

```
https://api.map.baidu.com/geocoder?address=<URL-encoded Chinese name>&output=html
```

It redirects to `map.baidu.com/mobile/?third_party=uri_api#...` — the mobile map
with the place searched, which offers to open the app. Verified working for
places, **metro stations** (`苏州地铁拙政园苏博站`), **exits**
(`南京东路站2号口`) and **lines** (`市域机场线`).

**Always search by name, never coordinates.** Baidu wants `lat,lng` in **BD-09**;
Amap wants `lng,lat` in **GCJ-02** — opposite on both counts, and a raw GPS
(WGS-84) figure is wrong in either by hundreds of metres.

**Escape ampersands as `&amp;` in href.** `&region=` parses as the entity `&reg;`
(®) otherwise — a real, silent bug.

Alternatives if the app doesn't open: `https://map.baidu.com/search/<name>` (web),
`baidumap://map/place/search?query=...&region=...&src=...` (app only, **dead link
if not installed**).

### Inline-linking place names — overlap-safe
Link the **first occurrence per section**, skipping anything already inside an
`<a>`. Critical: resolve all matches on the **clean text first**, reject
overlaps, then build the string once. Replacing in-place and re-searching creates
**nested anchors** (e.g. 北外滩 linked, then 外滩 linked *inside* it) — invalid
HTML that browsers mangle.

See `scripts/link_places.py`.

### Route diagrams
A hand-built inline **SVG** beats a real tile map on a phone: no library, no API
key, works with no signal, and **each stop can be a tappable link**. A bold
vertical thread with numbered dots, stop name, time, and the connector between
stops (`↓ walk 10 min`, `↓ 6号线`).

See `scripts/route_diagram.py`.

### Mobile navigation
A long itinerary needs a sticky bar + jump menu built from the headings, and a
back-to-top button. Two gotchas:
- An author-level `display:flex` **outranks** the UA's `[hidden]{display:none}` —
  restate `#el[hidden]{display:none}`.
- `scrollTo({behavior:'smooth'})` **silently does nothing** under
  reduced-motion — add an instant fallback.

### Date validation — always run this
Weekday labels are the easiest thing to get wrong and the most embarrassing.

```python
import re, datetime
S = {'Sun':6,'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5}
def check(text, year, month):
    bad = []
    for m in re.finditer(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]* (\d+)', text):
        d = datetime.date(year, month, int(m.group(2)))
        if d.weekday() != S[m.group(1)]:
            bad.append((m.group(0), d.strftime('%A')))
    return bad
```

Also sanity-check **internal consistency**: two dates N days apart cannot share a
weekday. Catch that before a calendar lookup.

---

## 4. Document structure that works

Order matters — put the things that expire first.

1. **Booking calendar** — every time-gated action with its date, most urgent
   first. This is the highest-value section.
2. **Before you go** — visa, arrival card, passport validity
3. **Internet and phone** — the firewall, roaming vs local SIM
4. **Paying on the ground** — 收款码 vs 付款码, the four rails, phrasebook
5. **Getting around** — airport transfer, metro, rail
6. **Flights and hotels** — with terminal, check-in floor, metro exits
7. **Day plans** — each with a route diagram, times, and inline map links
8. **Food** — with 人均 prices and opening hours; flag seasonal dishes
9. **Places quick-reference** — every name, tappable, as its own top-level
   section so it's one tap from the jump menu
10. **Weather/packing, practicalities, emergencies, medical**

**Give demanding days a Plan A / Plan B**, and state which bookings differ
between them — otherwise the traveller books before deciding and eats a
cancellation.

**Write in instructional voice, not chat voice.** "To buy a train ticket, first
create an account" — not "you need to register, that's what registration means".
Never let the document narrate its own edit history ("correcting what this page
said earlier").

**Put Chinese on everything operational** — place names, addresses, station
names, dish names, and the phrases for asking help. The traveller shows the
phone rather than pronouncing it.

---

## 5. Chinese that earns its place

Payments: **收款码** their code · **付款码** your code · **我扫你可以吗？** can I
scan yours instead · **支付失败了** payment failed · **我的是境外卡** mine is a
foreign card · **可以付现金吗？** can I pay cash · **不得拒收现金** refusing cash
is not permitted · **我要发票** official tax receipt

Transport: **乘车码** ride code · **单程票** single-journey ticket · **客服中心**
station service centre · **改签** change ticket · **人工现金通道** manual cash lane

Eating: **扫码点单** scan to order · **可以人工点单吗？** can I order with a
person · **有纸质菜单吗？** paper menu · **人均** per-head price

Help: **请帮我一下** please help me · **我不吃猪肉** I don't eat pork ·
**有清真的吗？** do you have halal

---

## 6. Checklist before shipping a China itinerary

- [ ] Every weekday label validated against the calendar
- [ ] No two dates N days apart sharing a weekday
- [ ] Every opening time and closure day verified against a Chinese source
- [ ] Booking windows dated, with the "book by" date stated, not just the rule
- [ ] Terminal confirmed for every flight
- [ ] Each day is one geographic corridor, not a criss-cross
- [ ] Museum/attraction closure days respected (Mondays are common)
- [ ] Seasonal dishes checked against travel dates
- [ ] Place names in Chinese, tappable, including stations and exits
- [ ] Payment stack explained with 收款码 / 付款码
- [ ] Roaming-vs-local-SIM stated as opposites
- [ ] Ampersands escaped in every href
- [ ] No nested anchors
- [ ] Rendered and measured at phone width — text ≥ body size, no sideways scroll
