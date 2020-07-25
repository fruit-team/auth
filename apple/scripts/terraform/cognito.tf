# Document: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cognito_user_pool
# IAM AmazonCognitoPowerUser permission required or you will see below error
# Error: Error creating Cognito User Pool: AccessDeniedException: User: arn:aws:iam::...:user/fruit_developer is not authorized to perform: cognito-idp:CreateUserPool on resource: *

resource "aws_cognito_user_pool" "user-pool" {
  alias_attributes        = ["email"]
  auto_verified_attributes = ["email"]
  mfa_configuration        = "OFF"
  name                    = "${var.name}_user_pool_${var.environment}"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
    temporary_password_validity_days = 7
  }

  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = false
    required            = true

    string_attribute_constraints {
      min_length = 5
      max_length = 2048
    }
  }

  lifecycle {
    ignore_changes = [schema]
  }
}

# Document: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cognito_user_pool_client
resource "aws_cognito_user_pool_client" "client" {
     name                = "${var.name}_user_pool_client_${var.environment}"
     user_pool_id        = aws_cognito_user_pool.user-pool.id
     generate_secret     = true
     explicit_auth_flows = ["ADMIN_NO_SRP_AUTH"]
 }

output "COGNITO_CLIENT_ID" {
  description = "aws congnito user pool client id"
  value       = "${aws_cognito_user_pool_client.client.id}"
}

output "COGNITO_CLIENT_SECRET" {
  description = "aws congnito user pool client secret"
  value       = "${aws_cognito_user_pool_client.client.client_secret}"
}
