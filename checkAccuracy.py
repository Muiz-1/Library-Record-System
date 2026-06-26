"""
checkAccuracy.py
----------------
For a given category, reads its evaluation CSV and reports:
  - Files that NEVER achieved accuracy=1.0  (with their best accuracy)
  - Files that DID achieve accuracy=1.0      (with the best combo: depth, episodes, time)

Usage:
    python checkAccuracy.py <Category>

Examples:
    python checkAccuracy.py Absence
    python checkAccuracy.py VaryingLen
"""

import csv
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FOLDER_CONFIGS = {
    'Absence':               'Absence',
    'Existence':             'Existence',
    'Universality':          'Universality',
    'VaryingForm':           'VaryingForm',
    'VaryingLen':            'VaryingLen',
    'VaryingSize':           'VaryingSize',
    'DisjunctionOfExistence':'DisjunctionOfExistence',
}

if len(sys.argv) < 2:
    print("Usage: python checkAccuracy.py <Category>")
    print(f"Categories: {', '.join(FOLDER_CONFIGS)}")
    sys.exit(1)

category = sys.argv[1]
if category not in FOLDER_CONFIGS:
    print(f"Unknown category '{category}'. Choose from: {', '.join(FOLDER_CONFIGS)}")
    sys.exit(1)

csv_path = os.path.join(SCRIPT_DIR, FOLDER_CONFIGS[category], 'evaluation_LTL4_seperately.csv')
if not os.path.exists(csv_path):
    print(f"CSV not found: {csv_path}")
    sys.exit(1)

# For each file: track best accuracy, and the combo that achieved acc=1.0 (if any)
best_acc   = {}   # file -> float
perfect    = {}   # file -> dict with depth/E/time for the first acc=1.0 row

with open(csv_path, newline='') as f:
    for row in csv.DictReader(f):
        fname = row['file']
        acc   = float(row['qpai_accuracy'])

        if fname not in best_acc or acc > best_acc[fname]:
            best_acc[fname] = acc

        if acc == 1.0 and fname not in perfect:
            perfect[fname] = {
                'depth': int(row['max_depth']),
                'E':     int(row['E']),
                'time':  float(row['qpai_time']),
            }

never_perfect  = {f: a for f, a in best_acc.items() if f not in perfect}
got_perfect    = {f: perfect[f] for f in best_acc if f in perfect}

print(f"\n{'='*60}")
print(f"  Category : {category}")
print(f"  CSV      : {csv_path}")
print(f"{'='*60}")

print(f"\n  Files that NEVER reached accuracy=1.0  ({len(never_perfect)} files)")
print(f"  {'File':<35}  {'Best Accuracy':>13}")
print('  ' + '-'*50)
for fname in sorted(never_perfect):
    print(f"  {fname:<35}  {never_perfect[fname]:>13.4f}")

print(f"\n  Files that DID reach accuracy=1.0  ({len(got_perfect)} files)")
print(f"  {'File':<35}  {'depth':>6}  {'E':>6}  {'time':>10}")
print('  ' + '-'*62)
for fname in sorted(got_perfect):
    p = got_perfect[fname]
    print(f"  {fname:<35}  {p['depth']:>6}  {p['E']:>6}  {p['time']:>9.3f}s")

print()
