.PHONY: start stop

start:
	@echo "Starting Flask server in a new terminal..."
	start cmd /c "cd News-System-BE && python3 -m flask run"

	@echo "Waiting for Flask server to start..."
	@timeout 5 /nobreak > nul

	@echo "Starting Frontend server in a new terminal..."
	start cmd /c "cd News-System-FE && npm start"
