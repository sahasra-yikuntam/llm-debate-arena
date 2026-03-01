install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
test:
	cd backend && pytest tests/ -v --cov=app --cov-report=term-missing
docker-up:
	docker-compose up --build
train:
	cd backend && python -m app.services.train_scorer
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f backend/debate_arena.db backend/test_debate.db
