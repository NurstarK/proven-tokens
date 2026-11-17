#!/bin/bash
# Copy tokens/aero to the build box and build the given Lake targets there (default: the whole
# project). Only tokens/aero is copied; no other folder of the kit on the box is touched.
# Usage: bash scripts/box.sh [target ...]     (for example: bash scripts/box.sh AeroVerify.Aero.Gen)
# Environment: BOX (default lean-ethlib-build), TAG (the name of the log, default aero).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BOX="${BOX:-lean-ethlib-build}"
VM="${VM:?set VM to your E2B box tool}"
TAG="${TAG:-aero}"
R=/home/user
TGZ="$(mktemp -t aero).tgz"
(cd "$ROOT/.." && COPYFILE_DISABLE=1 tar --exclude=.lake --exclude=__pycache__ --exclude=.DS_Store \
  -czf "$TGZ" aero)
python3 "$VM" put "$BOX" "$TGZ" "$R/aero-push.tgz" >/dev/null
rm -f "$TGZ"
python3 "$VM" exec "$BOX" --timeout 0 -- "
mkdir -p $R/logs && cd $R/token-kit/tokens && rm -rf aero/AeroVerify aero/scripts aero/config && tar xzf $R/aero-push.tgz 2>/dev/null
cat > $R/logs/$TAG.build.sh <<'B'
#!/bin/bash
export PATH=\$HOME/.elan/bin:\$PATH
echo \$\$ > $R/logs/$TAG.pid
cd $R/token-kit/tokens/aero
lake build \"\$@\" > $R/logs/$TAG.log 2>&1
echo \"EXIT=\$?\" >> $R/logs/$TAG.log
B
setsid nohup bash $R/logs/$TAG.build.sh $* >/dev/null 2>&1 </dev/null &
sleep 2
tail --pid=\$(cat $R/logs/$TAG.pid) -f /dev/null
grep -v 'module system\|^⚠\|^✔\|Replayed\|^warning: .*UsdtVerify\|^warning: .*EthLib' $R/logs/$TAG.log | grep -n -A12 '^error' | head -${LINES_MAX:-120}
tail -3 $R/logs/$TAG.log
df -m / | tail -1 | awk '{print \"disk free MB:\", \$4}'
"
