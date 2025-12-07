#!/usr/bin/env python3
"""
Helper to run the DP implementation in `4.py` using an input JSON file.

Usage:
  python run4.py                 # uses input_5.json by default
  python run4.py input_5.json    # or pass a custom input file path
"""
import sys
import json
import os
import importlib.util


def load_module_from_file(path, name='mod'):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, 'input_5.json')

    if not os.path.isabs(input_path):
        input_path = os.path.join(base, input_path)

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    # Load the 4.py implementation (module name mod4)
    mod4_path = os.path.join(base, '4.py')
    if not os.path.exists(mod4_path):
        print(f"Implementation file not found: {mod4_path}")
        sys.exit(1)

    mod4 = load_module_from_file(mod4_path, name='mod4')

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cap = int(data.get('capacity', 0))
    items = data.get('items', [])
    val = [int(it['v']) for it in items]
    wt = [int(it['w']) for it in items]

    # Call the DP function that returns (total_value, chosen_indices)
    if not hasattr(mod4, 'knapsack_with_items'):
        print('The module 4.py does not expose knapsack_with_items(cap, val, wt)')
        sys.exit(1)

    total, chosen = mod4.knapsack_with_items(cap, val, wt)

    print(f"Input: {os.path.basename(input_path)}  capacity={cap}  n_items={len(items)}")
    print(f"Max value: {total}")
    print(f"Chosen item indices: {chosen}")
    if chosen:
        print('Chosen items (w,v):')
        for idx in chosen:
            print(f"  - idx={idx} w={wt[idx]} v={val[idx]}")


if __name__ == '__main__':
    main()