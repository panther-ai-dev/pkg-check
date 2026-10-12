# Build log: "AI se fake package checker"

## Rules (fixed before start)
- Builder: Claude Code (Opus 5.5), one prompt, no human edits.
- Tool: Python, standard library only, one file.
- Done = it runs on a real requirements.txt and gives a correct verdict for real and made-up packages.

## Prompt
> Ek Python tool banao jo requirements.txt padhe aur har package PyPI pe check kare: exist karta hai ya nahi, kab bana, GitHub/source link hai ya nahi. Suspicious ho to warning do.

## Timeline
- 12:59:59 START
- 13:00:18 Code written (pkgcheck.py, standard library only)
- 13:00:52 Test 1: requests/numpy/flask OK; huggingface-cli and made-up django-smart-cache-xyz123 flagged NOT FOUND
- 13:00:52 Cross-checked huggingface-cli: PyPI web page looked like 200 but was a bot-check page; pip's own index returns 404 and pip install fails. Checker verdict correct.
- 13:01:05 Warning path tested (foo, hello: registered names with no files). Fixed duplicate warning ("no files" + "0 releases").
- 13:01:05 DONE. Total: 1 min 6 s

## Honest notes (what the reel must say)
- Works: real packages pass, made-up name caught, empty registered names warned. Standard library only, ~80 lines.
- huggingface-cli (the package from reel #5) is no longer installable from PyPI: JSON API 404, pip index 404, pip install fails. We don't know when or why it was removed, so the reel must not guess.
- Gotcha found while testing: the PyPI web page returned 200, but it was a bot-check page. Always check with pip's own index, not the website.
- One fix needed after the first run (duplicate warning). Code itself worked first time.
- The 90-day / 2-release / no-source-link rules are warnings, not proof. A brand-new real package will also get flagged.
- Not tested on a big real project file.

## Evidence
- run-output.txt (real output on requirements.txt)
