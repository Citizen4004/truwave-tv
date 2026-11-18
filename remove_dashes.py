#!/usr/bin/env python3
"""Remove em-dashes sitewide, replacing with natural punctuation."""
import re
import glob

def cap(m):
    return m.group(1).upper()

def fix_text(s):
    # Specific known short fragments -> natural rewording (handle before generic rule)
    s = s.replace('Get Started — WhatsApp', 'Get Started on WhatsApp')
    s = s.replace('— WhatsApp', 'on WhatsApp')

    # Title-ish pattern: "Short Title — Short Title" -> use a pipe (common, non-dash)
    def title_pipe(m):
        return f'{m.group(1)} | {m.group(2)}'
    s = re.sub(r'^([^—.]{3,60}) — ([^—.]{3,70})$', title_pipe, s, flags=re.M)

    # Paired dashes with NO link tag inside, same line only, reasonable length -> parentheses
    def paired(m):
        return f' ({m.group(1)}) '
    s = re.sub(r' — ((?:(?!<a )[^—\n]){1,100}?) — ', paired, s)

    # Generic single dash: prefer a period (new sentence) unless the clause after is a short fragment
    FRAGMENT_STARTS = ('not ', 'or ', 'and ', 'but ', 'just ', 'no ', 'nothing ')
    def generic(m):
        after = m.group(1)
        starts_fragment = after.lower().startswith(FRAGMENT_STARTS) or (after[0].isdigit())
        if len(after) <= 18 or starts_fragment:
            return ', ' + after[0].lower() + after[1:]
        else:
            return '. ' + after[0].upper() + after[1:]

    s = re.sub(r' — ([^—\n]+?)(?=[.!?]|<|$)', generic, s)

    # Any remaining stray em-dashes -> comma (rare, catch-all)
    s = s.replace(' — ', ', ')
    s = s.replace('—', ',')
    return s

files = glob.glob('**/*.html', recursive=True)
changed = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '—' not in content:
        continue
    new_content = fix_text(content)
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        changed.append(f)

print(f"Changed {len(changed)} files")
for f in changed:
    print(" -", f)
