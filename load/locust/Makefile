define DOCS
Run locust load test

Short run with debugging:       debug
Load test 1 user:               load-1
Load test 10 users:             load-10

Make sure port 8222 is forwarded
endef

LOCALHOST := 127.0.0.1
CHILLER_FRONTEND_PORT := 8222

export DOCS
docs:
	@echo "$$DOCS"

debug:
	 locust --headless --users 1 --spawn-rate 1 -H http://$(LOCALHOST):$(CHILLER_FRONTEND_PORT) --loglevel DEBUG --run-time 2s

load-1:
	 locust --headless --users 1 --spawn-rate 1 -H http://$(LOCALHOST):$(CHILLER_FRONTEND_PORT)

load-10:
	 locust --headless --users 10 --spawn-rate 10 -H http://$(LOCALHOST):$(CHILLER_FRONTEND_PORT)

