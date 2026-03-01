# ============================================================
# AUTOMATED SCORING SCRIPT
# Uses Claude API to automatically score all 80 responses
# using the same 4-dimension rubric as manual scoring.
#
# Methodology note: Automated scores are validated against
# manual scores on a 50% sample to assess inter-rater
# reliability — a standard academic validity check.
# ============================================================

import os
import json
import time
from dotenv import load_dotenv
import anthropic

# Load environment variables from .env file
load_dotenv()

# Initialise Anthropic client for Claude API
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================
# RUBRIC PROMPT TEMPLATE
# This prompt instructs Claude to score each response
# using the same criteria as the manual rubric
# ============================================================

def build_scoring_prompt(response_text, prompt_type, description):
	return f"""You are an expert evaluator assessing LLM responses for educational code debugging.

Score the following response across 4 dimensions. Return ONLY a JSON object with no extra text.

Context:
- Bug description: {description}
- Prompt type: {prompt_type} (direct = fix the bug, socratic = guide student with questions)

Response to evaluate:
{response_text}

Scoring rubric:

1. technical_accuracy (0-3):
   0 = incorrect or misleading
   1 = partially correct
   2 = correct but incomplete
   3 = fully correct and complete

2. explanation_clarity (0-3):
   0 = no explanation
   1 = confusing or unclear
   2 = understandable but could be clearer
   3 = clear and easy to follow

3. novice_appropriateness (0-3):
   0 = uses advanced concepts without explanation
   1 = somewhat appropriate but assumes too much knowledge
   2 = mostly appropriate for beginners
   3 = perfectly pitched for a novice programmer

4. socratic_scaffolding (0-3):
   0 = gives away the answer directly (expected for direct prompts)
   1 = minimal guidance toward solution
   2 = some guiding questions or hints
   3 = strong Socratic approach, guides without revealing answer

Return ONLY this JSON format:
{{
  "technical_accuracy": <0-3>,
  "explanation_clarity": <0-3>,
  "novice_appropriateness": <0-3>,
  "socratic_scaffolding": <0-3>,
  "reasoning": "<one sentence explaining your scores>"
}}"""

# ============================================================
# MAIN SCORING FUNCTION
# Sends each response to Claude API and parses the scores
# ============================================================

def auto_score_response(response_text, prompt_type, description):
	prompt = build_scoring_prompt(response_text, prompt_type, description)
    
	# Call Claude API
	message = client.messages.create(
		model="claude-sonnet-4-20250514",
		max_tokens=300,
		messages=[{"role": "user", "content": prompt}]
	)
    
	# Parse the JSON response
	raw = message.content[0].text.strip()
	scores = json.loads(raw)
	return scores

# ============================================================
# LOAD RESULTS AND RUN AUTO SCORING
# ============================================================

# Load all 80 benchmark results
results_path = "results/results.json"
auto_scores_path = "results/auto_scores.json"

results = []
with open(results_path, "r") as f:
	for line in f:
		line = line.strip()
		if line:
			results.append(json.loads(line))

print(f"Loaded {len(results)} results to score\n")

# Load existing auto scores to allow resume if interrupted
existing = {}
if os.path.exists(auto_scores_path):
	with open(auto_scores_path, "r") as f:
		for line in f:
			line = line.strip()
			if line:
				entry = json.loads(line)
				key = f"{entry['model']}_{entry['test_case_id']}_{entry['prompt_type']}"
				existing[key] = entry

print(f"Already scored: {len(existing)}\n")

# Score each response
for r in results:
	key = f"{r['model']}_{r['test_case_id']}_{r['prompt_type']}"
    
	# Skip already scored
	if key in existing:
		continue
    
	short_model = "GPT-4o" if "gpt" in r["model"] else "Llama 3"
	print(f"Scoring {short_model} | {r['test_case_id']} | {r['prompt_type']}...")
    
	try:
		# Get automated scores from Claude
		scores = auto_score_response(
			r["response"],
			r["prompt_type"],
			r["description"]
		)
        
		# Build score entry
		entry = {
			"model": r["model"],
			"test_case_id": r["test_case_id"],
			"description": r["description"],
			"prompt_type": r["prompt_type"],
			"technical_accuracy": scores["technical_accuracy"],
			"explanation_clarity": scores["explanation_clarity"],
			"novice_appropriateness": scores["novice_appropriateness"],
			"socratic_scaffolding": scores["socratic_scaffolding"],
			"reasoning": scores.get("reasoning", ""),
			"total_score": sum([
				scores["technical_accuracy"],
				scores["explanation_clarity"],
				scores["novice_appropriateness"],
				scores["socratic_scaffolding"]
			]),
			"scored_by": "claude-auto"
		}
        
		# Save to file
		with open(auto_scores_path, "a") as f:
			f.write(json.dumps(entry) + "\n")
        
		print(f"  Total: {entry['total_score']}/12 — {scores.get('reasoning', '')}")
        
		# Small delay to avoid rate limiting
		time.sleep(0.5)
        
	except Exception as e:
		print(f"  ERROR: {e}")
		continue

print("\nAuto scoring complete! Results saved to results/auto_scores.json")