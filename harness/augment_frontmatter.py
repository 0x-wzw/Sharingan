#!/usr/bin/env python3
"""Post-compile augmentation: inject author + version into compiled SKILL.md frontmatter.
Idempotent; reads book.author from the bundle's verified.yaml. Part of skillevaluator-harness."""
import re, sys, pathlib

def main(skill_dir):
    skill = pathlib.Path(skill_dir)
    md = skill / "SKILL.md"
    text = md.read_text(encoding="utf-8")
    # locate bundle verified.yaml next to workspace layout or sibling
    bundle = skill.parent.parent / "workspace/books"
    author = None
    for vy in (skill.parent.parent / "skills-src").glob("*/x"): pass
    # search known bundle path pattern
    for p in pathlib.Path.home().glob(".hermes/profiles/*/workspace/books/*/.cangjie/capabilities/verified.yaml"):
        b = p.read_text(encoding="utf-8")
        m = re.search(r"bundle_id:\s*"+re.escape(md.stem if False else "") , b)
        if "bundle." in text and re.search(r"bundle_id:\s*([\w\-.]+)", b):
            if re.search(r"entry:\s*\n\s*name:\s*(\S+)", b) and skill.name in b:
                a = re.search(r"^  author:\s*(.+)$", b, re.M)
                if a: author = a.group(1).strip(); break
    m = re.match(r"(---\n.*?\n---\n)", text, re.S)
    if not m:
        print("no frontmatter found"); return 1
    fm = m.group(1)
    changed = False
    if author and not re.search(r"^author:", fm, re.M):
        fm = fm.replace("metadata:\n", f"metadata:\n  author: \"{author}\"\n", 1); changed = True
    if changed:
        md.write_text(fm + text[m.end():], encoding="utf-8")
        print(f"augmented: author={author}")
    else:
        print("no changes needed")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
