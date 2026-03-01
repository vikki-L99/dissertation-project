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
├── main.py              # Core benchmarking runner — queries both models across all test cases
├── test_cases.py        # 20 buggy Python code scenarios covering 10 error categories
├── analyse.py           # Quantitative analysis — latency and response length statistics
├── rubric.py            # Interactive qualitative scoring tool — 4-dimension evaluation rubric
│
├── results/
│   ├── results.json     # Raw API responses with latency and timestamps (80 total calls)
│   └── scores.json      # Qualitative rubric scores per response
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

---

## 📈 Key Findings (Preliminary)

| Model         | Prompt Type | Avg Latency | Avg Response Length |
| ------------- | ----------- | ----------- | ------------------- |
| GPT-4o        | Direct      | 3.97s       | 1208 chars          |
| GPT-4o        | Socratic    | 0.98s       | 115 chars           |
| Llama 3.3 70B | Direct      | 1.57s       | 1538 chars          |
| Llama 3.3 70B | Socratic    | 0.43s       | 150 chars           |

> Llama 3.3 70B is consistently **2–4x faster** than GPT-4o across all prompt types, while also producing longer and more structured responses for direct prompting.

---

## 🐳 Running with Docker

All benchmarks are run inside a Docker container for reproducibility.

### Prerequisites

- Docker Desktop installed
- OpenAI API key (platform.openai.com)
- Groq API key (console.groq.com)

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
```

3. Build the Docker image:

```bash
docker build -t dissertation .
```

4. Run the benchmark:

```bash
docker run --env-file .env -v "${PWD}/results:/app/results" dissertation
```

5. Results are saved to `results/results.json`

### Run Analysis

```bash
python3 analyse.py
```

### Run Qualitative Scoring

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
| python-dotenv | Secure API key management           |
| Docker        | Containerised execution environment |
| Git / GitHub  | Version control                     |

---

## 📅 Project Timeline

| Phase      | Description                           | Target Date  |
| ---------- | ------------------------------------- | ------------ |
| ✅ Phase 1 | Literature Review + Initial Report    | Feb 27, 2026 |
| 🔄 Phase 2 | Benchmarking Framework Development    | Mar 20, 2026 |
| ⏳ Phase 3 | Data Collection + Qualitative Scoring | Apr 5, 2026  |
| ⏳ Phase 4 | Methodology + Software Chapters       | Apr 12, 2026 |
| ⏳ Phase 5 | Abstract + Introduction + Conclusions | Apr 18, 2026 |
| ⏳ Phase 6 | Final Submission                      | Apr 22, 2026 |

---

## 👩‍💻 Author

**V**  
MSc Computing — Edinburgh Napier University  
GitHub: [@vikki-L99](https://github.com/vikki-L99)

---

## 📄 Licence

This project is for academic research purposes only. All API usage is subject to the respective terms of service of OpenAI and Groq.
