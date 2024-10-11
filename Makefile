.PHONY: run
run:
	uvicorn main:app --reload --app-dir ./simple-chat-app/.
