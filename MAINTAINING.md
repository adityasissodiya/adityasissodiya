# Maintaining the website

Live site: https://adityasissodiya.github.io/adityasissodiya/

This repository is also the GitHub profile repository, so `README.md` is shown on
https://github.com/adityasissodiya. Keep it short; website documentation belongs here.

## How it works

| Path | Purpose |
| --- | --- |
| `content/site.toml` | **All page content.** The only file to edit for routine updates. |
| `build.py` | Renders `content/site.toml` into `_site/` (Python 3.11+, standard library only). |
| `assets/style.css` | Styles (light and dark, responsive). |
| `scripts/check.py` | Checks anchors, that every content URL is on the page, and that assets load under `/adityasissodiya/`. `--external` also requests every external link. |
| `.github/workflows/pages.yml` | On every push to `main`: build, check, and publish `_site/` to the `gh-pages` branch. |

GitHub Pages serves the `gh-pages` branch (Settings → Pages → Deploy from a branch →
`gh-pages` / root). Do not edit `gh-pages` by hand; it is overwritten on each deploy.

## Updating content

1. Edit `content/site.toml` (directly on GitHub is fine). Comments in the file explain each field.
2. When you have reviewed the statuses, set `site.status_date` to that day. The page shows it as
   "Last updated". Do not change it for typo or style fixes.
3. Commit to `main`. The workflow deploys within a minute or two; check the Actions tab if not.

To preview locally:

```sh
python3 build.py && python3 scripts/check.py
mkdir -p /tmp/preview && ln -sfn "$PWD/_site" /tmp/preview/adityasissodiya
python3 -m http.server -d /tmp/preview 8000   # open http://localhost:8000/adityasissodiya/
```

### Common edits

- **Paper accepted or published:** remove its `[[research]]` block and add a `[[publications]]`
  block (newest first). Keep code and preprint links.
- **New manuscript title:** replace `label`, update `label_note`, and remove the item from
  `to_confirm` and from `[todo]`.
- **Next actions:** edit `[[actions]]`. Keep `kind = "suggested"` until the action is agreed;
  then use `kind = "confirmed"` and set `target_date = "YYYY-MM-DD"`. Leave dates empty when unknown.
- **Courses:** fill `title`, `code`, `credits`, `period` from the official course record only.
  Canvas page numbers are not course codes. Add completed courses as further `[[courses]]` blocks.
- **Videos:** put the MP4 (H.264/AAC, under ~50 MB), a poster JPEG and a `.vtt` caption file in
  `assets/video/`, then add a `video = { ... }` line to the research entry (see the rescue-ois entry).
- **Status colours:** `status_key` is one of `preparation`, `exploratory`, `review`,
  `published`, `ongoing`, `todo`. The visible text comes from `status_label`.
- **Never publish Overleaf share links** (`.../share#...`, `overleaf.com/read/...`): they grant access
  to anyone holding them. Use the plain `https://www.overleaf.com/project/<id>` address.
- **Private links:** add `access = "sign-in"` to links that need sign-in (Overleaf, Canvas, ISP).
  Listing a link does not grant access to it, but it does make the address public.

## Provenance of the current content (as of 28 October 2026)

- Statuses of ongoing work, the Casper collaboration and all working links: supplied by Aditya
  on 2026-10-28. The contents of Overleaf, Canvas and the ISP were not inspected.
- Project summaries for rescue-ois and Agents and access control: paraphrased from each public
  repository's README (checked 2026-10-28). The target venue and working title quoted there are
  marked "to confirm" on the page.
- Publication and thesis metadata: DiVA records diva2:1991066 and diva2:2020653, and the
  SCITEPRESS record for DOI 10.5220/0013130000003899. One-line summaries paraphrase the abstracts.
- EQuack (IEEE Internet of Things Journal): title, author order, article type and submission
  date (3 June 2026) from the journal's submission overview, supplied by Aditya on 2026-10-28.
  The one-line summary paraphrases the submitted abstract and the public licentiate thesis.
  Co-author emails, funding details and manuscript files are deliberately not published.
- rescue-ois manuscript title and author order: supplied by Aditya on 2026-10-28. The video
  (`assets/video/`) and its captions were supplied by Aditya the same day; the captions are
  converted from the supplied SRT file. Replace `research.video` paths to swap the video.
- Task-Scoped Authorization: working title, Casper Lundberg's LTU profile and the Overleaf
  project supplied by Aditya on 2026-10-28. The Overleaf share token in the supplied link was
  deliberately left out; the page links the plain project URL, which requires sign-in.
- Thesis supervisors are as listed in the thesis; the current supervisory team is not stated.

## Maintenance checklist (information still missing)

- [ ] Target venue and submission date for rescue-ois
- [ ] Agreed scope and author list of the Task-Scoped Authorization paper (with Casper Lundberg)
- [ ] Course title, official code, credits, period, assessment deadlines
- [ ] Completed and planned courses; credit totals
- [ ] Current doctoral supervisory team
- [ ] Next ISP review date; doctoral thesis milestones
- [ ] Optional: code/data links for published papers, Google Scholar, CV
