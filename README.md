# 🏛️ LLM Debate Arena

[![CI](https://github.com/sahasra-yikuntam/llm-debate-arena/actions/workflows/ci.yml/badge.svg)](https://github.com/sahasra-yikuntam/llm-debate-arena/actions)

An automated framework that pits two LLMs against each other in structured debates, then scores argument quality using a fine-tuned DistilBERT classifier — making LLM evaluation cheap, scalable, and reproducible.

## What It Does

1. **Debate Generation** — Two LLM agents take opposing sides on a topic and exchange structured arguments
2. **LLM Judge** — A third LLM scores each argument on 4 axes: Logical Coherence, Factual Grounding, Rhetorical Strength, and Fallacy Detection
3. **ML Scorer** — A fine-tuned DistilBERT model replaces the expensive LLM judge for fast, scalable inference
4. **React Dashboard** — Live debate viewer with real-time scoring visualization

## Tech Stack

Python · FastAPI · PyTorch · HuggingFace Transformers · DistilBERT · React · SQLite · Docker · GitHub Actions

## Quick Start
```bash
git clone https://github.com/sahasra-yikuntam/llm-debate-arena.git
cd llm-debate-arena
cp .env.example .env
# Add your API keys to .env
docker-compose up --build
```

## Why This Matters

LLM evaluation is one of the hardest unsolved problems in AI. This project demonstrates scalable eval by replacing expensive LLM-as-judge calls with a fine-tuned lightweight model — exactly what teams at Anthropic, OpenAI, and Google are working on.

Built by Sahasra Yikuntam
