# Personal OS

Your private vault: inbox, context layer, meeting notes, 1:1s, tasks, projects and `outputs/` for ad-hoc files.

**What is shared and what stays yours.** The rules (`.cursor/rules/`), router files, scripts, templates and empty folders come with the repo and update for every PM through `/update-product-os`. Everything you write here is gitignored: it is never committed or pushed.

## First run

From the repo root:

```bash
bash 01_product-os/onboarding/setup-personal.sh
```

It copies the starter files (context stubs, task lists, meeting routing) from `99_System/templates/vault/` into place. It never overwrites a file. Then say `set me up` in a chat: it fills `99_System/context/` and `99_System/meetings/routing.json` from your calendar, one question at a time.

Day to day: `morning brief`, `sync meetings`, `plan my week`.

## Optional later

- `extras/eod/`: nightly digest (launchd). Turn on after two weeks of briefs.
- `extras/gsd/`: team weekly-goals board if your org uses that process.

## Shared vs personal

Would another Phenom PM need this with no extra explanation? If yes, promote it to `01_product-os/` (`promote context`, which opens a pull request). If no, it stays here.

## Changing what every PM gets

Edit a rule, script or starter file here and open a pull request. Never put names, meetings or goals in a tracked file.
