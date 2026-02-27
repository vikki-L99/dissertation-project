# def hello():
# 	return "Dissertation project is alive!"
# print(hello())

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(buggy_code, prompt_type="direct"):
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
		"prompt_type": prompt_type,
		"latency_seconds": latency,
		"timestamp": datetime.now().isoformat(),
		"response": response.choices[0].message.content
	}
    
	return result

# Test
buggy_code = """
def calculate_average(numbers):
	total = 0
	for n in numbers:
		total = total + n
	return total / len(numbers)

print(calculate_average([]))
"""

result = ask_gpt(buggy_code, "direct")
print(f"Latency: {result['latency_seconds']}s")
print(f"Response:\n{result['response']}")

# Save to log file
with open("results.json", "a") as f:
	f.write(json.dumps(result) + "\n")

print("\nResult saved to results.json!")