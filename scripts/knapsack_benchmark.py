"""
Knapsack benchmark runner

Usage examples:
  # Run on an existing input file
  python knapsack_benchmark.py --input input.json --output results.csv

  # Generate random instance (n items) and run
  python knapsack_benchmark.py --generate --n 25 --capacity 100 --output results.csv

The script will attempt to load the four implementations located in the same
directory as this script (`1.py`, `2.py`, `3.py`, `4.py`) and call the
function `knapsack(W, val, wt)` exported by each module. Because filenames
start with digits, modules are loaded by file path using importlib utilities.

The script saves timing results to a CSV and prints a short summary.
"""
import argparse
import json
import os
import time
import csv
import random
import traceback
import importlib.util
import types


def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_implementations(base_dir):
    impls = []
    for i in range(1, 5):
        filename = os.path.join(base_dir, f"{i}.py")
        if os.path.exists(filename):
            try:
                mod = load_module_from_path(f"impl_{i}", filename)
                if hasattr(mod, 'knapsack'):
                    impls.append((f"impl_{i}", mod.knapsack, filename))
                else:
                    print(f"Warning: {filename} has no `knapsack` function")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"Note: {filename} not found; skipping")
    return impls


def read_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Expect {"capacity": int, "items": [{"w":int, "v":int}, ...]}
    cap = int(data.get('capacity', 0))
    items = data.get('items', [])
    val = [int(it['v']) for it in items]
    wt = [int(it['w']) for it in items]
    return cap, val, wt


def write_example_input(path, n=10, capacity=50, max_w=20, max_v=100, seed=None):
    if seed is not None:
        random.seed(seed)
    items = []
    for _ in range(n):
        w = random.randint(1, max_w)
        v = random.randint(1, max_v)
        items.append({"w": w, "v": v})
    data = {"capacity": capacity, "items": items}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Wrote example input to {path} (n={n}, capacity={capacity})")


def benchmark(impls, cap, val, wt, timeout=None):
    # Run each implementation and time it. timeout (seconds) not enforced per-call,
    # but we abort if a single run takes longer than timeout (checked after run).
    results = []
    for name, fn, src in impls:
        record = {"impl": name, "capacity": cap, "n_items": len(val), "status": "ok", "time": None, "result": None, "error": None}
        try:
            t0 = time.perf_counter()
            res = fn(cap, val, wt)
            t1 = time.perf_counter()
            elapsed = t1 - t0
            record['time'] = elapsed
            record['result'] = res
            if timeout is not None and elapsed > timeout:
                record['status'] = 'timeout'
        except RecursionError as re:
            record['status'] = 'recursion_error'
            record['error'] = str(re)
        except Exception as e:
            record['status'] = 'error'
            record['error'] = ''.join(traceback.format_exception_only(type(e), e)).strip()
        results.append(record)
        print(f"{name}: status={record['status']} time={record['time']} result={record['result']}")
    return results


def save_results_csv(path, rows):
    keys = ['impl', 'capacity', 'n_items', 'status', 'time', 'result', 'error']
    write_header = True
    # If the file exists and has content, append without writing the header
    if os.path.exists(path) and os.path.getsize(path) > 0:
        write_header = False

    # Open in append mode so existing rows are preserved
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if write_header:
            writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, '') for k in keys})
    if write_header:
        print(f"Created and saved results to {path}")
    else:
        print(f"Appended {len(rows)} result(s) to {path}")


def parse_args():
    p = argparse.ArgumentParser(description='Knapsack implementations benchmark runner')
    p.add_argument('--input', '-i', default='input.json', help='Path to input JSON file')
    p.add_argument('--generate', action='store_true', help='Generate a new input file and exit')
    p.add_argument('--n', type=int, default=10, help='Number of items to generate')
    p.add_argument('--capacity', type=int, default=50, help='Knapsack capacity to generate/use')
    p.add_argument('--max-weight', type=int, default=20, help='Max item weight when generating')
    p.add_argument('--max-value', type=int, default=100, help='Max item value when generating')
    p.add_argument('--seed', type=int, default=None, help='Random seed for generation')
    p.add_argument('--output', '-o', default='results.csv', help='CSV path to write results')
    p.add_argument('--timeout', type=float, default=10.0, help='Per-implementation soft timeout in seconds (reported only)')
    return p.parse_args()


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.generate:
        write_example_input(args.input, n=args.n, capacity=args.capacity, max_w=args.max_weight, max_v=args.max_value, seed=args.seed)
        print("Generation complete. Run without --generate to benchmark the implementations.")
        return

    if not os.path.exists(args.input):
        print(f"Input file {args.input} not found. You can create one with --generate")
        return

    cap, val, wt = read_input(args.input)
    impls = load_implementations(base_dir)
    if not impls:
        print("No valid implementations were loaded. Ensure 1.py..4.py exist in the same directory and expose `knapsack(W, val, wt)`.")
        return

    print(f"Loaded {len(impls)} implementations. Items={len(val)} Capacity={cap}")
    results = benchmark(impls, cap, val, wt, timeout=args.timeout)
    save_results_csv(args.output, results)


if __name__ == '__main__':
    main()