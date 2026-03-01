# 🔬 LLM Benchmarking Framework for Educational Code Debugging

> **MSc Computing Dissertation** — Edinburgh Napier University  
> _Benchmarking Large Language Models for Educational Code Debugging: A Comparative Analysis of Direct vs Socratic Prompting Strategies_

---

## 📋 Overview

This repository contains the benchmarking framework developed for my MSc dissertation. The framework systematically evaluates and compares two large language models — **GPT-4o** (OpenAI) and **Llama 3.3 70B** (Meta, via Groq) — across two distinct prompting strategies:

- **Direct Prompting** — The model is asked to identify and fix the bug directly
- **Socratic Prompting** — The model is asked to guide the student toward the answer through questioning

The goal is to determine which model and prompting strategy is most effective for **educational code debugging** in a novice programming context.

---

## 🏗️ Architecture

```
dissertation-project/
│
├── main.py              # Core benchmarking runner — auto-detects run number and queries both models
├── test_cases.py        # 20 buggy Python code scenarios covering 10 error categories
├── analyse.py           # Quantitative analysis — latency and response length statistics
├── auto_score.py        # Automated qualitative scoring via Claude API — scores all responses
├── rubric.py            # Interactive manual scoring tool — 4-dimension evaluation rubric
├── summary.py           # Summary statistics — averaged scores across all runs
│
├── results/
│   ├── results.jsonl      # Raw API responses with latency, timestamps and run numbers
│   └── auto_scores.jsonl  # Automated qualitative rubric scores per response
│
├── Dockerfile           # Container definition — Python 3.11-slim base
├── requirements.txt     # Python dependencies
└── .env                 # API keys (not tracked in git)
```

---

## 🧪 Test Cases

20 buggy Python code scenarios covering 10 common novice error categories:

| Category                       | Test Cases   |
| ------------------------------ | ------------ |
| Division / ZeroDivision errors | TC001, TC011 |
| Index / Range errors           | TC002, TC012 |
| Mutable default arguments      | TC003        |
| Logic / Indentation errors     | TC004, TC015 |
| Type errors                    | TC005, TC017 |
| Variable scope errors          | TC006, TC013 |
| Infinite loops                 | TC007, TC014 |
| Missing return values          | TC008        |
| List mutation during iteration | TC009        |
| Boolean logic errors           | TC010        |
| List method misuse             | TC016        |
| String/integer comparison      | TC018        |
| Dictionary key errors          | TC019        |
| Variable shadowing             | TC020        |

---

## 📊 Evaluation Methodology

### Quantitative Metrics

- **Response Latency** — Time in seconds from API call to response
- **Response Length** — Character count as a proxy for verbosity

### Qualitative Rubric (0–3 per dimension, max 12/12)

| Dimension              | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| Technical Accuracy     | Is the bug correctly identified and fixed?              |
| Explanation Clarity    | Is the explanation clear and understandable?            |
| Novice Appropriateness | Is the response pitched correctly for a beginner?       |
| Socratic Scaffolding   | Does the response guide without giving away the answer? |

### Scoring Approach

Qualitative scoring was conducted using an **automated rubric applied via the Claude API**, with manual validation available via `rubric.py` for inter-rater reliability assessment. All benchmarks were conducted across **3 independent trials** to ensure result reliability and account for API response variability.

---

## 📈 Key Findings (3-Run Average, 240 Total Responses)

### Latency Comparison

| Model         | Prompt Type | Avg Latency | Avg Response Length |
| ------------- | ----------- | ----------- | ------------------- |
| GPT-4o        | Direct      | ~3.50s      | ~1208 chars         |
| GPT-4o        | Socratic    | ~0.95s      | ~115 chars          |
| Llama 3.3 70B | Direct      | ~1.55s      | ~1538 chars         |
| Llama 3.3 70B | Socratic    | ~0.40s      | ~150 chars          |

### Quality Scores (out of 12)

| Model         | Prompt Type | Avg Score |
| ------------- | ----------- | --------- |
| GPT-4o        | Direct      | 8.66/12   |
| GPT-4o        | Socratic    | 11.25/12  |
| Llama 3.3 70B | Direct      | 8.58/12   |
| Llama 3.3 70B | Socratic    | 11.63/12  |

> **Key findings:** Llama 3.3 70B matches GPT-4o on direct prompting quality while outperforming it on Socratic prompting, at 2–4x lower latency. Both models score significantly higher on Socratic prompting than direct prompting, suggesting Socratic strategies produce higher quality educational responses regardless of model choice.

---

## 🐳 Running with Docker

All benchmarks are run inside a Docker container for reproducibility.

### Prerequisites

- Docker Desktop installed
- OpenAI API key (platform.openai.com)
- Groq API key (console.groq.com)
- Anthropic API key (console.anthropic.com) — for automated scoring

### Setup

1. Clone the repository:

```bash
git clone https://github.com/vikki-L99/dissertation-project.git
cd dissertation-project
```

2. Create your `.env` file:

```bash
OPENAI_API_KEY=your-openai-key-here
GROQ_API_KEY=your-groq-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

3. Build the Docker image:

```bash
docker build -t dissertation .
```

4. Run the benchmark (auto-detects run number):

```bash
docker run --env-file .env -v "${PWD}/results:/app/results" dissertation
```

5. Results are saved to `results/results.jsonl`

### Run Automated Scoring

```bash
python3 auto_score.py
```

### Run Summary Statistics

```bash
python3 summary.py
```

### Run Quantitative Analysis

```bash
python3 analyse.py
```

### Run Manual Scoring (optional validation)

```bash
python3 rubric.py
```

---

## 🛠️ Tech Stack

| Tool          | Purpose                             |
| ------------- | ----------------------------------- |
| Python 3.11   | Core language                       |
| OpenAI SDK    | GPT-4o API integration              |
| Groq SDK      | Llama 3.3 70B API integration       |
| Anthropic SDK | Claude API for automated scoring    |
| python-dotenv | Secure API key management           |
| Docker        | Containerised execution environment |
| Git / GitHub  | Version control                     |

---

## 📅 Project Timeline

| Phase      | Description                           | Target Date  |
| ---------- | ------------------------------------- | ------------ |
| ✅ Phase 1 | Literature Review + Initial Report    | Feb 27, 2026 |
| ✅ Phase 2 | Benchmarking Framework Development    | Mar 20, 2026 |
| ⏳ Phase 3 | Data Collection + Qualitative Scoring | Apr 5, 2026  |
| ⏳ Phase 4 | Methodology + Software Chapters       | Apr 12, 2026 |
| ⏳ Phase 5 | Abstract + Introduction + Conclusions | Apr 18, 2026 |
| ⏳ Phase 6 | Final Submission                      | Apr 22, 2026 |

---

## 👩‍💻 Author

**Aung Htet Myet Kyaw (Viktoria)**  
MSc Computing — Edinburgh Napier University  
GitHub: [@vikki-L99](https://github.com/vikki-L99)

---

## 📄 Licence

This project is for academic research purposes only. All API usage is subject to the respective terms of service of OpenAI, Groq, and Anthropic.
