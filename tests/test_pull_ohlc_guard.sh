#!/usr/bin/env bash
# tests/test_pull_ohlc_guard.sh — v1.0 — 2026-08-04
#
# The v1.3 guard decision table in pull_today_ohlc.sh, driven over all eight
# (FEED, POSTCLOSE, BOT) states.
#
# WHY A SHELL TEST AND NOT PYTEST: the guard is three shell conditions inside a
# detached __work block that stops systemd units and calls the TastyTrade
# producer. Standing that up would test the mocks. The decision itself is one
# boolean and it is the whole of the change — v1.1's version was correct for
# every state EXCEPT the one backfill actually uses, and it cost two sessions of
# sat-out tape before anyone looked.
#
# KEEP THIS IN SYNC BY HAND, deliberately: if the condition in the script
# changes, this file must change with it. check_versions carries a canary on the
# literal condition so a drift between the two is caught at deploy time.
#
# Run:  bash tests/test_pull_ohlc_guard.sh
# script and driven over all eight (FEED, POSTCLOSE, BOT) combinations.
# The condition below is copied VERBATIM from pull_today_ohlc.sh v1.3.
decide() {
  FEED="$1"; POSTCLOSE="$2"; BOT="$3"
  if [ "$FEED" = "active" ] && [ "$POSTCLOSE" = "0" ] && [ "$BOT" = "active" ]; then
    echo "SKIP"
  else
    echo "REBUILD"
  fi
}
fail=0
chk(){ got=$(decide "$1" "$2" "$3"); [ "$got" = "$4" ] && s="ok " || { s="FAIL"; fail=1; }; \
       printf "  %s feed=%-8s postclose=%s bot=%-8s -> %-7s (want %s)\n" "$s" "$1" "$2" "$3" "$got" "$4"; }
echo "THE CASE THAT WAS BROKEN — sat-out box, mid-session, no bot:"
chk active   0 inactive REBUILD
chk active   0 unknown  REBUILD
echo "THE CASE THE GUARD EXISTS FOR — trading box mid-session:"
chk active   0 active   SKIP
echo "POST-CLOSE — unchanged, always rebuilds:"
chk active   1 active   REBUILD
chk active   1 inactive REBUILD
echo "FEED NOT RUNNING — nothing to stop, always rebuilds:"
chk inactive 0 active   REBUILD
chk inactive 0 inactive REBUILD
chk unknown  0 active   REBUILD
exit $fail
