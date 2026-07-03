# Dutray Yorkies Static Rebuild

Clean static rebuild starter for Dutray Yorkies.

## Current setup
- Static HTML/CSS/JS
- Puppy listings live in `data/puppies.json`
- Admin starter files live in `/admin` for Decap CMS, but GitHub OAuth must be configured before daughter/editor login will work.
- Contact form currently uses a Formspree placeholder in `contact.html`.

## Local preview
Use VS Code Live Server or run:

```bash
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## Cloudflare Pages
Recommended deploy path: GitHub repo connected to Cloudflare Pages.
Build command: leave blank.
Build output directory: `/` or root.
