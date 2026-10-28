#!/usr/bin/env python3
"""Build the static website from content/site.toml into _site/.

Standard library only (Python 3.11+). Usage: python3 build.py [--out _site]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import shutil
import tomllib
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "site.toml"
ASSETS = ROOT / "assets"

NAV = [
    ("research", "Research"),
    ("next-actions", "Next actions"),
    ("publications", "Publications"),
    ("thesis", "Licentiate thesis"),
    ("courses", "Courses"),
    ("study-planning", "Study planning"),
    ("links", "Links"),
]

STATUS_KEYS = {"preparation", "exploratory", "review", "published", "ongoing", "todo"}


def e(text: str) -> str:
    return html.escape(text, quote=True)


def fmt_date(value: str) -> str:
    """Format YYYY-MM-DD as '28 October 2026'; pass other values (e.g. a year) through."""
    try:
        d = dt.date.fromisoformat(value)
    except ValueError:
        return value
    return f"{d.day} {d.strftime('%B %Y')}"


def unknown(text: str = "To add") -> str:
    return f'<span class="unknown">{e(text)}</span>'


def value_or_unknown(value: str, text: str = "To add") -> str:
    return e(value) if value else unknown(text)


def status(key: str, label: str) -> str:
    if key not in STATUS_KEYS:
        raise ValueError(f"unknown status_key {key!r}; use one of {sorted(STATUS_KEYS)}")
    return f'<span class="status status-{key}">{e(label)}</span>'


def link(item: dict) -> str:
    url, label = item["url"], item["label"]
    external = urlparse(url).scheme in {"http", "https"}
    attrs = ' rel="noopener"' if external else ""
    out = f'<a href="{e(url)}"{attrs}>{e(label)}</a>'
    if item.get("access") == "sign-in":
        out += ' <span class="access">Sign-in may be required</span>'
    return out


def link_list(items: list[dict], cls: str = "links") -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{link(i)}</li>" for i in items)
    return f'<ul class="{cls}">{lis}</ul>'


def render_profile(c: dict, base: str) -> str:
    p = c["profile"]
    links = list(p["links"]) + [{"label": p["email"], "url": f"mailto:{p['email']}"}]
    photo = ""
    if p.get("photo"):
        photo = (
            f'<img class="portrait" src="{base}{e(p['photo'])}" alt="{e(p.get('photo_alt', ''))}"'
            ' width="480" height="480">'
        )
    return f"""
<section class="profile" aria-labelledby="name">
  {photo}
  <div class="profile-text">
  <h1 id="name">{e(p['name'])}</h1>
  <p class="role">{e(p['role'])}<br>{e(p['affiliation'])}</p>
  <p class="lede">{e(p['focus'])}</p>
  {link_list(links, 'profile-links')}
  <p class="updated">Content status as of <time datetime="{e(c['site']['status_date'])}">{fmt_date(c['site']['status_date'])}</time></p>
  </div>
</section>"""


def render_video(v: dict, base: str) -> str:
    captions = ""
    if v.get("captions"):
        captions = f'<track kind="captions" src="{base}{e(v["captions"])}" srclang="en" label="English">'
    return f"""
    <figure class="video">
      <video controls preload="none" playsinline poster="{base}{e(v['poster'])}" aria-label="{e(v['title'])}">
        <source src="{base}{e(v['src'])}" type="video/mp4">
        {captions}
        <a href="{base}{e(v['src'])}">Download the video (MP4)</a>
      </video>
      <figcaption><strong>{e(v['title'])}.</strong> {e(v['caption'])}</figcaption>
    </figure>"""


def render_research(c: dict, base: str) -> str:
    cards = []
    for r in c["research"]:
        video = render_video(r["video"], base) if r.get("video") else ""
        summary = f"<p>{e(r['summary'])}</p>" if r.get("summary") else ""
        confirm = ""
        if r.get("to_confirm"):
            items = "".join(f"<li>{e(t)}</li>" for t in r["to_confirm"])
            confirm = f'<div class="to-confirm"><p class="small-heading">To confirm</p><ul>{items}</ul></div>'
        cards.append(f"""
  <article class="card{' card-wide' if video else ''}">
    <div class="card-head">
      <h3>{e(r['label'])}</h3>
      {status(r['status_key'], r['status_label'])}
    </div>
    <p class="meta">{e(r['label_note'])}</p>
    {f'<p class="authors">{e(r["authors"])}</p>' if r.get("authors") else ""}
    <p>{e(r['status_detail'])}</p>
    {summary}
    {video}
    {confirm}
    {link_list(r.get('links', []))}
  </article>""")
    date = fmt_date(c["site"]["status_date"])
    return f"""
<section id="research" aria-labelledby="research-h">
  <h2 id="research-h">Ongoing research</h2>
  <p class="section-note">Statuses as reported on {date}. Working labels will be replaced by manuscript titles when available.</p>
  <div class="cards">{''.join(cards)}
  </div>
</section>"""


def render_actions(c: dict) -> str:
    rows = []
    for a in c["actions"]:
        kind = a["kind"]
        if kind not in {"suggested", "confirmed"}:
            raise ValueError(f"action kind must be 'suggested' or 'confirmed', got {kind!r}")
        kind_html = f'<span class="kind kind-{kind}">{kind.capitalize()}</span>'
        date = (
            f'<time datetime="{e(a["target_date"])}">{fmt_date(a["target_date"])}</time>'
            if a.get("target_date")
            else unknown("Not set")
        )
        rows.append(f"""
      <tr>
        <th scope="row" data-label="Effort">{e(a['effort'])}</th>
        <td data-label="Next action">{e(a['next_action'])}</td>
        <td data-label="Type">{kind_html}</td>
        <td data-label="Target date">{date}</td>
      </tr>""")
    no_dates = "" if any(a.get("target_date") for a in c["actions"]) else " No target dates have been set yet."
    return f"""
<section id="next-actions" aria-labelledby="actions-h">
  <h2 id="actions-h">Next actions</h2>
  <p class="section-note"><strong>Suggested</strong> actions are planning prompts, not commitments. <strong>Confirmed</strong> actions have been agreed.{no_dates}</p>
  <div class="table-wrap">
  <table class="stack">
    <thead><tr><th scope="col">Effort</th><th scope="col">Next action</th><th scope="col">Type</th><th scope="col">Target date</th></tr></thead>
    <tbody>{''.join(rows)}
    </tbody>
  </table>
  </div>
</section>"""


def render_publications(c: dict) -> str:
    items = []
    for p in c["publications"]:
        items.append(f"""
  <li class="pub">
    <h3>{e(p['title'])}</h3>
    <p class="authors">{e(p['authors'])}</p>
    <p class="venue"><cite>{e(p['venue'])}</cite>, {e(p['details'])}, {e(p['year'])}.
      <span class="status status-published">Published</span> <span class="meta">{e(p['type'])}</span></p>
    <p>{e(p['summary'])}</p>
    {link_list(p.get('links', []))}
  </li>""")
    return f"""
<section id="publications" aria-labelledby="pubs-h">
  <h2 id="pubs-h">Publications</h2>
  <ol class="pubs" reversed>{''.join(items)}
  </ol>
</section>"""


def render_thesis(c: dict) -> str:
    t = c["thesis"]
    return f"""
<section id="thesis" aria-labelledby="thesis-h">
  <h2 id="thesis-h">Licentiate thesis</h2>
  <article class="pub">
    <h3>{e(t['title'])}</h3>
    <p class="authors">{e(t['author'])}</p>
    <p class="venue">{e(t['type'])}, {e(t['institution'])}, {e(t['year'])}.
      <span class="status status-published">Published</span></p>
    <p>{e(t['summary'])}</p>
    <p><strong>Supervisors:</strong> {e(t['supervisors'])}. <span class="meta">{e(t['supervisors_note'])}</span></p>
    {link_list(t.get('links', []))}
  </article>
</section>"""


def render_courses(c: dict) -> str:
    rows = []
    for k in c["courses"]:
        title = e(k["title"]) if k["title"] else f"Current LTU course {unknown('title to add')}"
        rows.append(f"""
      <tr>
        <th scope="row" data-label="Course">{title}</th>
        <td data-label="Code">{value_or_unknown(k['code'])}</td>
        <td data-label="Credits">{value_or_unknown(k['credits'])}</td>
        <td data-label="Period">{value_or_unknown(k['period'])}</td>
        <td data-label="Status">{status(k['status_key'], k['status_label'])}</td>
        <td data-label="Workspace">{''.join(link(l) for l in k.get('links', []))}</td>
      </tr>""")
    notes = "".join(f"<li>{e(k['note'])}</li>" for k in c["courses"] if k.get("note"))
    return f"""
<section id="courses" aria-labelledby="courses-h">
  <h2 id="courses-h">Courses</h2>
  <div class="table-wrap">
  <table class="stack">
    <thead><tr><th scope="col">Course</th><th scope="col">Code</th><th scope="col">Credits</th><th scope="col">Period</th><th scope="col">Status</th><th scope="col">Workspace</th></tr></thead>
    <tbody>{''.join(rows)}
    </tbody>
  </table>
  </div>
  <ul class="notes">{notes}<li>Completed and planned courses will be added from the official study record.</li></ul>
</section>"""


def render_study(c: dict) -> str:
    s = c["study"]
    rows = []
    for m in s["milestones"]:
        state = unknown(m["state"]) if m["state"].lower().startswith("to ") else e(m["state"])
        rows.append(f"""
      <tr>
        <th scope="row" data-label="Milestone">{e(m['milestone'])}</th>
        <td data-label="Status">{state}</td>
        <td data-label="Date">{value_or_unknown(fmt_date(m['date']) if m['date'] else '', 'Not set')}</td>
      </tr>""")
    isp = link({"label": "Individual Study Plan (ISP)", "url": s["isp_url"], "access": "sign-in"})
    return f"""
<section id="study-planning" aria-labelledby="study-h">
  <h2 id="study-h">Study planning</h2>
  <p>{isp}</p>
  <div class="table-wrap">
  <table class="stack">
    <thead><tr><th scope="col">Milestone</th><th scope="col">Status</th><th scope="col">Date</th></tr></thead>
    <tbody>{''.join(rows)}
    </tbody>
  </table>
  </div>
</section>"""


def render_links(c: dict) -> str:
    p = c["profile"]
    public = list(p["links"]) + [{"label": f"Email: {p['email']}", "url": f"mailto:{p['email']}"}]
    working = [l for r in c["research"] for l in r.get("links", []) if l.get("access") == "sign-in"]
    working += [l for k in c["courses"] for l in k.get("links", [])]
    working.append({"label": "Individual Study Plan (ISP)", "url": c["study"]["isp_url"], "access": "sign-in"})
    return f"""
<section id="links" aria-labelledby="links-h">
  <h2 id="links-h">Links</h2>
  <div class="two-col">
    <div>
      <h3>Public</h3>
      {link_list(public, 'links vertical')}
    </div>
    <div>
      <h3>Working resources</h3>
      {link_list(working, 'links vertical')}
      <p class="meta">Overleaf, Canvas and ISP pages are private workspaces. They may require sign-in or project permission; listing them here does not grant access.</p>
    </div>
  </div>
</section>"""


def render_todo(c: dict) -> str:
    items = c.get("todo", {}).get("items", [])
    if not items:
        return ""
    lis = "".join(f"<li>{e(t)}</li>" for t in items)
    return f"""
<details class="todo">
  <summary>Details still to add ({len(items)})</summary>
  <ul>{lis}</ul>
</details>"""


def page(c: dict, body: str, base: str, title: str | None = None) -> str:
    s = c["site"]
    nav = "".join(f'<li><a href="{base}#{i}">{e(t)}</a></li>' for i, t in NAV)
    favicon = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
        "%3Crect width='32' height='32' rx='6' fill='%231f4e79'/%3E%3Ctext x='16' y='22' "
        "font-family='Georgia,serif' font-size='16' fill='white' text-anchor='middle'%3EAS%3C/text%3E%3C/svg%3E"
    )
    photo = c["profile"].get("photo")
    og_image = f'<meta property="og:image" content="{e(s["base_url"] + photo)}">' if photo else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title or s['title'])}</title>
<meta name="description" content="{e(s['description'])}">
<link rel="canonical" href="{e(s['base_url'])}">
<meta property="og:title" content="{e(s['title'])}">
<meta property="og:description" content="{e(s['description'])}">
<meta property="og:url" content="{e(s['base_url'])}">
<meta property="og:type" content="profile">
{og_image}
<link rel="icon" href="{favicon}">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}">{e(s['title'])}</a>
    <nav aria-label="Sections"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main" class="wrap" tabindex="-1">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>Last updated <time datetime="{e(s['status_date'])}">{fmt_date(s['status_date'])}</time>.
    Source on <a href="https://github.com/adityasissodiya/adityasissodiya">GitHub</a>.</p>
  </div>
</footer>
</body>
</html>
"""


def build(out: Path) -> None:
    with CONTENT.open("rb") as f:
        c = tomllib.load(f)
    base = urlparse(c["site"]["base_url"]).path  # e.g. /adityasissodiya/
    if not base.endswith("/"):
        raise ValueError("site.base_url must end with '/'")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ASSETS, out / "assets")
    (out / ".nojekyll").write_text("")

    body = "".join([
        render_profile(c, base),
        render_research(c, base),
        render_actions(c),
        render_publications(c),
        render_thesis(c),
        render_courses(c),
        render_study(c),
        render_links(c),
        render_todo(c),
    ])
    (out / "index.html").write_text(page(c, body, base), encoding="utf-8")

    not_found = f"""
<section class="profile">
  <h1>Page not found</h1>
  <p>This address does not exist. <a href="{base}">Go to the home page</a>.</p>
</section>"""
    (out / "404.html").write_text(page(c, not_found, base, "Page not found · " + c["site"]["title"]), encoding="utf-8")
    print(f"Built {out}/index.html for base path {base}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(ROOT / "_site"))
    build(Path(ap.parse_args().out))
