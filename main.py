# def hello():
# 	return "Dissertation project is alive!"
# print(hello())

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
from test_cases import TEST_CASES

load_dotenv()
os.makedirs("results", exist_ok=True)

# # Run number for tracking multiple trials
# # Change this to 2 and 3 for subsequent runs
# RUN_NUMBER = 1

# Auto-detect run number by checking existing results
# This automatically increments each time the benchmark runs
def get_run_number():
	if not os.path.exists("results/results.jsonl"):
		return 1
	runs = set()
	with open("results/results.jsonl", "r") as f:
		for line in f:
			if line.strip():
				r = json.loads(line)
				if "run" in r:
					runs.add(r["run"])
	return max(runs) + 1 if runs else 1

RUN_NUMBER = get_run_number()
print(f"Starting Run {RUN_NUMBER}...")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(buggy_code, prompt_type):
	if prompt_type == "direct":
		return f"Fix this Python code and explain what was wrong:\n\n{buggy_code}"
	else:
		return f"A student wrote this Python code. Ask them one Socratic question to help them find the bug themselves:\n\n{buggy_code}"

def ask_gpt(test_case, prompt_type="direct"):
	prompt = build_prompt(test_case["buggy_code"], prompt_type)
    
	start_time = time.time()
	response = openai_client.chat.completions.create(
		model="gpt-4o",
		messages=[{"role": "user", "content": prompt}]
	)
	latency = round(time.time() - start_time, 3)
    
	return {
		"model": "gpt-4o",
		"run": RUN_NUMBER,
		"test_case_id": test_case["id"],
		"description": test_case["description"],
		"prompt_type": prompt_type,
		"latency_seconds": latency,
		"timestamp": datetime.now().isoformat(),
		"response": response.choices[0].message.content
	}

def ask_llama(test_case, prompt_type="direct"):
	prompt = build_prompt(test_case["buggy_code"], prompt_type)
    
	start_time = time.time()
	response = groq_client.chat.completions.create(
		model="llama-3.3-70b-versatile",
		messages=[{"role": "user", "content": prompt}]
	)
	latency = round(time.time() - start_time, 3)
    
	return {
		"model": "llama-3.3-70b-versatile",
		"run": RUN_NUMBER,
		"test_case_id": test_case["id"],
		"description": test_case["description"],
		"prompt_type": prompt_type,
		"latency_seconds": latency,
		"timestamp": datetime.now().isoformat(),
		"response": response.choices[0].message.content
	}

# Run all test cases for both models
for test_case in TEST_CASES:
	for prompt_type in ["direct", "socratic"]:
		print(f"GPT-4o  | {test_case['id']} - {prompt_type}...")
		result = ask_gpt(test_case, prompt_type)
		print(f"  Latency: {result['latency_seconds']}s")
		with open("results/results.jsonl", "a") as f:
			f.write(json.dumps(result) + "\n")

		print(f"Llama 3 | {test_case['id']} - {prompt_type}...")
		result = ask_llama(test_case, prompt_type)
		print(f"  Latency: {result['latency_seconds']}s")
		with open("results/results.jsonl", "a") as f:
			f.write(json.dumps(result) + "\n")

print("\nAll tests complete! Results saved to results.jsonl")