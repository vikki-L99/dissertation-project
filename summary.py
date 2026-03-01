import json
from collections import defaultdict

# Load auto scores
scores = []
with open('results/auto_scores.json', 'r') as f:
	for line in f:
		if line.strip():
			scores.append(json.loads(line))

# Group and average by model and prompt type
grouped = defaultdict(list)
for s in scores:
	key = (s['model'], s['prompt_type'])
	grouped[key].append(s['total_score'])

print('=' * 55)
print('Model                     Prompt       Avg Score')
print('=' * 55)
for (model, prompt_type), totals in sorted(grouped.items()):
	avg = sum(totals) / len(totals)
	short = 'GPT-4o' if 'gpt' in model else 'Llama 3'
	print(f'{short:<25} {prompt_type:<12} {avg:>7.2f}/12')
print('=' * 55)