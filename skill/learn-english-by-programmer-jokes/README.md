# Standalone Hermes Skill Bundle

This folder is a self-contained Hermes skill package for `learn-english-by-programmer-jokes`.

## Local install

Copy the whole `learn-english-by-programmer-jokes/` folder into your local Hermes skills directory:

```bash
cp -a learn-english-by-programmer-jokes ~/.hermes/skills/
hermes skills list | grep -i learn-english-by-programmer-jokes
```

Then preload it with:

```bash
hermes chat -s learn-english-by-programmer-jokes -q 'Summarize what I just fixed'
```

## Publish

This directory is also suitable as a standalone skill artifact for skill hubs such as ClawHub, because it already contains:

- `SKILL.md`
- generated `references/`
- `templates/`
- helper `scripts/`
- minimal `utils/` runtime code
- local `jokes_with_id.csv` data source
