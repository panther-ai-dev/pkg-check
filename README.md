# pkg-check: catch fake / hallucinated Python packages

Built for the **@panther_ai_dev** reel *AI Build Diaries #7: "AI se fake package checker"*.

AI coding tools sometimes suggest package names that don't exist, and attackers register those names ("slopsquatting"). `pkgcheck.py` reads a `requirements.txt` and checks every package against PyPI before you install anything.

## Built with AI
- **Builder:** Claude Code (Opus 5.5), one prompt, no human edits
- **Prompt (as given):**
  > Ek Python tool banao jo requirements.txt padhe aur har package PyPI pe check kare: exist karta hai ya nahi, kab bana, GitHub/source link hai ya nahi. Suspicious ho to warning do.
- **Time:** 1 min 6 s from prompt to tested tool. Timeline in [LOG.md](LOG.md).

## Run it
Python 3, standard library only:
```bash
python pkgcheck.py requirements.txt
```
Real output on the sample file ([run-output.txt](run-output.txt)):
```
[OK] requests
[OK] numpy
[OK] flask
[XX] huggingface-cli: does NOT exist on PyPI. Do not install.
[XX] django-smart-cache-xyz123: does NOT exist on PyPI. Do not install.

5 checked, 2 not found.
```

## Honest notes
- The age / release-count / source-link rules are **warnings, not proof**. A brand-new real package will also get flagged.
- One fix was needed after the first run (a duplicate warning). The rest of the code worked the first time.
- Not tested on a big real project's requirements file.

Follow [@panther_ai_dev](https://instagram.com/panther_ai_dev) for the reel.
