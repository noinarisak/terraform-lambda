.DEFAULT_GOAL := help

.PHONY: build
build: ## Build
	@echo "+ $@"

.PHONY: clean-pyc
clean-tfstate: ## Remove terraform state files
	@echo "+ $@"
	@find . -type f -name '*.tfstate*' -exec rm -f {} +

.PHONY: clean
clean: clean-tfstate ## Cleanup files
	@echo "+ $@"

.PHONY: update
update: ## Update okta tenant
	@echo "+ $@"
	@terraform init -backend-config=config/backend.conf

.PHONY: plan
plan: ## Plann okta tenant
	@echo "+ $@"
	@terraform plan -var-file=config/prod.tfvars

.PHONY: apply
apply: update plan ## Apply changes to okta tenant
	@echo "+ $@"
	@terraform apply -var-file=config/prod.tfvars

.PHONY: destroy
destroy: ## Destroy okta tenant
	@echo "+ $@"
	@terraform destroy -var-file=config/prod.tfvars -lock=false

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'