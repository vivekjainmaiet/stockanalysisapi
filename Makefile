# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

install:
	@pip install . -U

build_docker:
	@docker build -t stockanalysisapi .

run_docker:
	@docker run -e PORT=8080 -p 8001:8080 stockanalysisapi

run_api:
	@uvicorn api:app --reload --port 8002
