deploy: setup
	@cd scripts/terraform && terraform apply
	@source ./venv/bin/activate && chalice deploy --stage dev

clean:
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

destroy: setup
	@source ./venv/bin/activate && chalice delete --stage dev
	@cd scripts/terraform && terraform destroy

setup:
ifeq (,$(wildcard ~/.aws/config))
	@brew install awscli
	@aws configure
endif
ifeq (,$(wildcard ./scripts/terraform/.terraform))
	@brew install terraform
	@cd scripts/terraform && terraform init
endif
ifeq (,$(wildcard ./venv))
	@python3 -m pip install virtualenv
	@python3 -m virtualenv venv
	@source venv/bin/activate && pip install -r requirements.txt
endif

.PHONY: deploy clean destroy setup
