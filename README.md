# uchumeow.github.io

uchumeow's early-2000s personal homepage with a self-hosted visitor counter.

## Website

GitHub Pages serves the files in the repository root at:

https://uchumeow.github.io

To preview it locally:

```bash
python -m http.server
```

Open http://localhost:8000.

## Visitor counter on archpad

The counter is a small FastAPI service with a persistent SQLite database. It counts once per browser using local storage and does not store visitor IP addresses.

On `archpad`:

```bash
git clone https://github.com/uchumeow/uchumeow.github.io.git
cd uchumeow.github.io/counter
doas docker compose -f compose.yml up -d --build
curl http://127.0.0.1:8098/health
doas tailscale funnel --bg --https=8443 http://127.0.0.1:8098
```

The website is already configured to use:

```text
https://archpad.tail29a9cb.ts.net:8443
```

This uses Funnel port `8443`, so the existing Jellyfin Funnel on port `443` stays unchanged.

To check the counter:

```bash
curl https://archpad.tail29a9cb.ts.net:8443/api/count
```

To stop the counter:

```bash
cd uchumeow.github.io/counter
doas docker compose -f compose.yml down
doas tailscale funnel --https=8443 off
```
