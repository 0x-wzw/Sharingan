#!/usr/bin/env python3
"""Vault mirror sync — reference implementation from the Ubuntu VM cangjie stack.

Mirrors every `source:`-marked skill into the Obsidian vault, rebuilds the index,
and cuts a content-hash bundle release on the skills repo. Machine defaults are
Zehan's Ubuntu VM; override via env: VB_VAULT_DIR, VB_SKILLS_DIR, VB_GH_REPO.
Shares the fail-closed secret-scan discipline with harness_sync.py.
(Cron 04:10 on the VM; see harness_sync.py for the whole-VM machine variant.)
"""
# The full implementation lives at https://github.com/0x-wzw/hermes-harness (scripts/cangjie_skill_sync.py)
# — committed here as the documented reference pointer to keep the two estates from forking.
raise SystemExit("reference pointer — run the VM copy: ~/.hermes/scripts/cangjie_skill_sync.py")
