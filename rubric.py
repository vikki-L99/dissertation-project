# ============================================================
# QUALITATIVE SCORING RUBRIC
# Manually scores each LLM response across 4 dimensions:
#
# 1. Technical Accuracy (0-3)
#    0 = incorrect or misleading
#    1 = partially correct
#    2 = correct but incomplete
#    3 = fully correct and complete
#
# 2. Explanation Clarity (0-3)
#    0 = no explanation
#    1 = confusing or unclear
#    2 = understandable but could be clearer
#    3 = clear and easy to follow
#
# 3. Novice Appropriateness (0-3)
#    0 = uses advanced concepts without explanation
#    1 = somewhat appropriate but assumes too much
#    2 = mostly appropriate for beginners
#    3 = perfectly pitched for a novice programmer
#
# 4. Socratic Scaffolding (0-3)
#    0 = gives away the answer directly
#    1 = minimal guidance toward solution
#    2 = some guiding questions or hints
#    3 = strong Socratic approach, guides without revealing
#
# Maximum score per response: 12
# ============================================================

import json
import os

# --- Load results ---
results_path = "results/results.jsonl"

results = []
with open(results_path, "r") as f:
	for line in f:
		line = line.strip()
		if line:
			results.append(json.loads(line))

# --- Score storage ---
# Scores will be saved to results/scores.jsonl
scores_path = "results/scores.jsonl"

# Load existing scores so we don't re-score already scored responses
existing_scores = {}
if os.path.exists(scores_path):
	with open(scores_path, "r") as f:
		for line in f:
			line = line.strip()
			if line:
				score = json.loads(line)
				# Use model + test_case_id + prompt_type as unique key
				key = f"{score['model']}_{score['test_case_id']}_{score['prompt_type']}"
				existing_scores[key] = score

print(f"Loaded {len(results)} results")
print(f"Already scored: {len(existing_scores)}")
print("\nScoring instructions:")
print("Enter a score 0-3 for each dimension, or 's' to skip\n")

# --- Scoring loop ---
for r in results:
	key = f"{r['model']}_{r['test_case_id']}_{r['prompt_type']}"
    
	# Skip already scored responses
	if key in existing_scores:
		continue
    
	# Display the response for scoring
	short_model = "GPT-4o" if "gpt" in r["model"] else "Llama 3"
	print("\n" + "=" * 60)
	print(f"Model: {short_model} | Test: {r['test_case_id']} | Type: {r['prompt_type']}")
	print(f"Description: {r['description']}")
	print("-" * 60)
	print(f"RESPONSE:\n{r['response']}")
	print("-" * 60)
    
	# Get scores from user
	scores = {}
	dimensions = [
		"technical_accuracy",
		"explanation_clarity", 
		"novice_appropriateness",
		"socratic_scaffolding"
	]
    
	skip = False
	for dim in dimensions:
		while True:
			val = input(f"Score {dim} (0-3) or 's' to skip: ").strip()
			if val == 's':
				skip = True
				break
			if val in ['0', '1', '2', '3']:
				scores[dim] = int(val)
				break
			print("Please enter 0, 1, 2, or 3")
		if skip:
			break
    
	if skip:
		continue
    
	# Calculate total score
	total = sum(scores.values())
    
	# Save score
	score_entry = {
		"model": r["model"],
		"test_case_id": r["test_case_id"],
		"description": r["description"],
		"prompt_type": r["prompt_type"],
		**scores,
		"total_score": total
	}
    
	with open(scores_path, "a") as f:
		f.write(json.dumps(score_entry) + "\n")
    
	print(f"Saved! Total score: {total}/12")

print("\nScoring complete!")