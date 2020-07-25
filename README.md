# Apple
Authentication service of fruit.team

## Quick Start

### Setup
```
$ cd PATH/TO/WORKING/DIRECTORY/ROOT
$ git clone https://github.com/fruit-team/auth.git
$ cd auth/apple
$ make setup
```

### Deploy
```
$ cd PATH/TO/WORKING/DIRECTORY/ROOT
$ cd auth/apple
$ make congnito
# You can see this outputs
COGNITO_CLIENT_ID = ****
COGNITO_CLIENT_SECRET = ****

# Edit apple/.chalice/config.json
{
  ...
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "environment_variables": {
        "STAGE": "dev",
        "COGNITO_CLIENT_ID": "****",    <------------------ COGNITO_CLIENT_ID
        "COGNITO_CLIENT_SECRET": "****" <------------------ COGNITO_CLIENT_SECRET
      }
    },
    "staging": {
      "api_gateway_stage": "api"
    },
    "prod": {
      "api_gateway_stage": "api"
    }
  }
}

$ make deploy
```

### Destroy all AWS services
```
$ make destroy
...
Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes <------------------ yes
```