# Swagger YAML

This directory contains a swagger YAML built by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project.

It was set up automatically through [`Github Sync`](https://app.swaggerhub.com/help/integrations/github-sync) integration on Swaggerhub.

# Design and Documentation
The API spec can be publicly viewed [here](https://app.swaggerhub.com/apis/BrightHive/program-registry) and is hosted [here](https://docs.brighthive.io/v1.0/reference#organization).

The folder [.openapi](/openapi) was generated automatically by SwaggerHub. We have set up [`Github Sync`](https://app.swaggerhub.com/help/integrations/github-sync) for the API spec on Swaggerhub. It promises to automatically update the spec on Github with changes done in SwaggerrHub. The API design and documentation process, therefore, is that all stakeholders collaborate on SwaggerHub and the update is synced on Github upon save.

> NB

We noted however that this integration is still buggy (It doesn't sync with Github on save). The integration works well for setting up this workflow for a new repo. So we activated [`Github Push`](https://app.swaggerhub.com/help/integrations/github-push) for the syncing. The spec file is at [.openapi/swagger.yaml](.openapi/swagger.yaml).

### To adopt this workflow

For a similar workflow, you'll find that the docs in [`Github Push`](https://app.swaggerhub.com/help/integrations/github-push) and [`Github Sync`](https://app.swaggerhub.com/help/integrations/github-sync) are quite straight forward.

Be sure to set:
- a separate branch other that the main ones (In our case we chose *SWAGGERHUB*)
- swagger output folder as `.openapi` and 
- swagger file as `swagger.yaml`
