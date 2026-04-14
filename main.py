# ============================================================
# main.py - Core Benchmarking Runner
#
# This script is the entry point for the dissertation
# benchmarking framework. It:
#   1. Auto-detects the current run number
#   2. Queries GPT-4o (OpenAI) and Llama 3.3 70B (Groq)
#   3. Tests each model across 20 buggy Python code scenarios
#   4. Tests both Direct and Socratic prompting strategies
#   5. Logs latency, timestamps and full responses to JSONL
#
# Usage (inside Docker):
#   docker run --env-file .env -v "${PWD}/results:/app/results" dissertation
#
# Output:
#   results/results.jsonl - one JSON record per line
# ============================================================

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
from test_cases import TEST_CASES

# --- Environment Setup ---
# Load API keys from .env file into environment variables
load_dotenv()

# Ensure results directory exists before writing any output
os.makedirs("results", exist_ok=True)

# --- File Paths ---
RESULTS_FILE = "results/results.jsonl"

# ============================================================
# RUN NUMBER AUTO-DETECTION
# Reads existing results to determine which run number to use.
# This ensures each benchmark run is properly labelled
# without requiring manual configuration changes.
# ============================================================

def get_run_number():
	"""
	Automatically determines the next run number by reading
	existing results. Returns 1 if no results exist yet.
	"""
	if not os.path.exists(RESULTS_FILE):
		return 1

	runs = set()
	with open(RESULTS_FILE, "r") as f:
		for line in f:
			if line.strip():
				record = json.loads(line)
				if "run" in record:
					runs.add(record["run"])

	return max(runs) + 1 if runs else 1


# Determine and display current run number
RUN_NUMBER = get_run_number()
print(f"Starting Run {RUN_NUMBER}...")

# ============================================================
# API CLIENT INITIALISATION
# Both clients are initialised once at startup using API keys
# loaded from the .env file via load_dotenv() above.
# ============================================================

# OpenAI client for GPT-4o
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Groq client for Llama 3.3 70B
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================================================
# PROMPT BUILDER
# Constructs the prompt sent to each model based on the
# prompting strategy being tested:
#   - direct:   Ask the model to fix the bug and explain
#   - socratic: Ask the model to guide the student with a question
# ============================================================

def build_prompt(buggy_code, prompt_type):
	"""
	Builds the prompt string for a given prompting strategy.

	Args:
		buggy_code (str): The buggy Python code snippet
		prompt_type (str): Either 'direct' or 'socratic'

	Returns:
		str: The formatted prompt to send to the model
	"""
	if prompt_type == "direct":
		return f"Fix this Python code and explain what was wrong:\n\n{buggy_code}"
	else:
		return f"A student wrote this Python code. Ask them one Socratic question to help them find the bug themselves:\n\n{buggy_code}"


# ============================================================
# MODEL QUERY FUNCTIONS
# Each function sends a prompt to its respective model,
# measures response latency, and returns a structured result.
# ============================================================

def ask_gpt(test_case, prompt_type="direct"):
	"""
	Queries GPT-4o with a buggy code test case.

	Args:
		test_case (dict): Test case containing id, description, buggy_code
		prompt_type (str): Either 'direct' or 'socratic'

	Returns:
		dict: Structured result with model info, latency and response
	"""
	prompt = build_prompt(test_case["buggy_code"], prompt_type)

	# Record start time before API call for latency measurement
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
	"""
	Queries Llama 3.3 70B via Groq API with a buggy code test case.

	Args:
		test_case (dict): Test case containing id, description, buggy_code
		prompt_type (str): Either 'direct' or 'socratic'

	Returns:
		dict: Structured result with model info, latency and response
	"""
	prompt = build_prompt(test_case["buggy_code"], prompt_type)

	# Record start time before API call for latency measurement
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


# ============================================================
# MAIN BENCHMARK LOOP
# Iterates over all test cases and both prompt types,
# queries both models, and appends results to the JSONL file.
# Each result is saved immediately so progress is not lost
# if the script is interrupted.
# ============================================================

for test_case in TEST_CASES:
	for prompt_type in ["direct", "socratic"]:

		# --- Query GPT-4o ---
		print(f"GPT-4o  | {test_case['id']} - {prompt_type}...")
		result = ask_gpt(test_case, prompt_type)
		print(f"  Latency: {result['latency_seconds']}s")

		# Append result immediately to avoid data loss on interruption
		with open(RESULTS_FILE, "a") as f:
			f.write(json.dumps(result) + "\n")

		# --- Query Llama 3.3 70B ---
		print(f"Llama 3 | {test_case['id']} - {prompt_type}...")
		result = ask_llama(test_case, prompt_type)
		print(f"  Latency: {result['latency_seconds']}s")

		# Append result immediately to avoid data loss on interruption
		with open(RESULTS_FILE, "a") as f:
			f.write(json.dumps(result) + "\n")

print(f"\nRun {RUN_NUMBER} complete! Results saved to {RESULTS_FILE}")