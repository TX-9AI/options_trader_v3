#!/bin/bash
# =============================================================================
# install_tooling.sh — make a CHECKOUT's tooling runnable, with no controller.
# v1.1 — 2026-07-30 — +pytest. It was never in requirements.txt nor verified
#        here, so `python -m pytest tests/` on control failed repeatedly with
#        "No module named pytest" — a provisioning gap, not a command mistake.
# v1.0 — 2026-07-30
#
# WHY THIS EXISTS
#   Every bot in this fleet runs independently — there is no requirement for a
#   controller to exist at all. So the repo has to be able to provision its own
#   tooling wherever it is cloned, not only where setup_ec2.sh happened to run.
#
#   setup_ec2.sh STEP 7 already installs requirements.txt into a venv, so a FULL
#   install has always been covered. What was never covered is a BARE CHECKOUT —
#   a clone used as a source of tools rather than as a running bot. The control
#   server's ~/options-trader-v3 is exactly that, and on 2026-07-30 push.sh v1.8
#   gained a hard dependency on pyflakes for its undefined-name gate. Nothing had
#   ever installed this repo's dependencies there, so the gate could not run and
#   push.sh correctly refused every push.
#
#   That is not a bug in the gate — refusing is the designed behaviour, because a
#   guard that silently skips is the exact failure class it was written to catch
#   (continuation `mid` 07-29, butterfly `_mult` 07-30). It is a gap in
#   provisioning, and this closes it.
#
# WHAT IT DOES
#   Installs requirements.txt with whatever python is active — the repo venv if
#   one exists, otherwise the system interpreter. Then VERIFIES the tools the
#   repo's own scripts depend on actually import. Idempotent; safe to re-run.
#
# USAGE
#   bash install_tooling.sh            # from anywhere; resolves its own repo
# =============================================================================
set -u

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ="$REPO_DIR/requirements.txt"

echo -e "${BOLD}${CYAN}  options_trader — tooling bootstrap${RESET}"
echo "  repo: $REPO_DIR"

if [ ! -f "$REQ" ]; then
    echo -e "  ${RED}✗  requirements.txt not found at $REQ${RESET}"
    exit 1
fi

# Prefer the repo's venv when one exists (a full setup_ec2.sh install); fall back
# to whatever python is on PATH (a bare checkout, e.g. the control server).
if [ -x "$REPO_DIR/venv/bin/python" ]; then
    PY="$REPO_DIR/venv/bin/python"; WHICH="repo venv"
elif command -v python3 >/dev/null 2>&1; then
    PY="$(command -v python3)"; WHICH="system python3"
else
    echo -e "  ${RED}✗  no python3 found${RESET}"; exit 1
fi
echo -e "  python: $PY  ${CYAN}($WHICH)${RESET}"

echo "  installing requirements…"
if ! "$PY" -m pip install -r "$REQ" -q 2>/dev/null; then
    # A system interpreter on Ubuntu 24.04 is externally managed (PEP 668).
    echo -e "  ${YELLOW}⚠  plain install refused — retrying with"
    echo -e "     --break-system-packages (PEP 668 externally-managed env)${RESET}"
    "$PY" -m pip install -r "$REQ" -q --break-system-packages || {
        echo -e "  ${RED}✗  install failed${RESET}"; exit 1; }
fi

# Verify the tools this repo's OWN scripts depend on. Listed explicitly rather
# than inferred, so a silent drop from requirements.txt is caught here instead of
# at the moment some script needs it.
#
# pytest is here because control kept failing `python -m pytest tests/` with
# "No module named pytest" through late July. Root cause was never a bad command:
# ~/.bashrc activates the day_trader_pro venv, otv3's suite runs in that shell,
# and NOTHING had ever installed pytest into it. Provisioning beats remembering.
FAILED=0
for mod in pyflakes pytest; do
    if "$PY" -c "import $mod" 2>/dev/null; then
        echo -e "  ${GREEN}✓  $mod importable${RESET}"
    else
        echo -e "  ${RED}✗  $mod NOT importable after install${RESET}"
        FAILED=1
    fi
done

if [ "$FAILED" -ne 0 ]; then
    echo -e "  ${RED}✗  tooling incomplete — push.sh's undefined-name gate"
    echo -e "     will refuse to run.${RESET}"
    exit 1
fi

echo -e "  ${GREEN}${BOLD}✓  tooling ready — push.sh gate armed${RESET}"
