# def hello():
# 	return "Dissertation project is alive!"
# print(hello())

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from test_cases import TEST_CASES

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(test_case, prompt_type="direct"):
	buggy_code = test_case["buggy_code"]
    
	if prompt_type == "direct":
		prompt = f"Fix this Python code and explain what was wrong:\n\n{buggy_code}"
	else:
		prompt = f"A student wrote this Python code. Ask them one Socratic question to help them find the bug themselves:\n\n{buggy_code}"
    
	start_time = time.time()
    
	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[{"role": "user", "content": prompt}]
	)
    
	end_time = time.time()
	latency = round(end_time - start_time, 3)
    
	result = {
		"model": "gpt-4o",
		"test_case_id": test_case["id"],
		"description": test_case["description"],
		"prompt_type": prompt_type,
		"latency_seconds": latency,
		"timestamp": datetime.now().isoformat(),
		"response": response.choices[0].message.content
	}
    
	return result

# Run all test cases
for test_case in TEST_CASES:
	for prompt_type in ["direct", "socratic"]:
		print(f"Running {test_case['id']} - {prompt_type}...")
		result = ask_gpt(test_case, prompt_type)
		print(f"  Latency: {result['latency_seconds']}s")
        
		with open("results.json", "a") as f:
			f.write(json.dumps(result) + "\n")

print("\nAll tests complete! Results saved to results.json")