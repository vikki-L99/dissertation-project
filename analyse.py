import json
import os
from collections import defaultdict

# ============================================================
# ANALYSIS SCRIPT
# Reads results.jsonl and calculates:
# 1. Average latency per model per prompt type
# 2. Average response length per model per prompt type
# 3. Summary table for dissertation evaluation chapter
# ============================================================

# --- Load results from file ---
results_path = "results/results.jsonl"

if not os.path.exists(results_path):
	print("No results file found. Run main.py first.")
	exit()

results = []
with open(results_path, "r") as f:
	for line in f:
		line = line.strip()
		if line:  # skip empty lines
			results.append(json.loads(line))

print(f"Loaded {len(results)} results\n")

# --- Group results by model and prompt type ---
# defaultdict lets us group without checking if key exists first
grouped = defaultdict(list)
for r in results:
	key = (r["model"], r["prompt_type"])
	grouped[key].append(r)

# --- Calculate averages ---
print("=" * 60)
print(f"{'Model':<30} {'Prompt':<12} {'Avg Latency':>12} {'Avg Resp Len':>13}")
print("=" * 60)

for (model, prompt_type), entries in sorted(grouped.items()):
	# Calculate average latency in seconds
	avg_latency = sum(e["latency_seconds"] for e in entries) / len(entries)
    
	# Calculate average response length in characters
	avg_response_len = sum(len(e["response"]) for e in entries) / len(entries)
    
	# Shorten model name for display
	short_model = "GPT-4o" if "gpt" in model else "Llama 3"
    
	print(f"{short_model:<30} {prompt_type:<12} {avg_latency:>11.3f}s {avg_response_len:>12.0f}c")

print("=" * 60)
print("\nNote: Response length measured in characters (c)")