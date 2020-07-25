# Apple
Authentication service of fruit.team

## Quick Start

### Setup AWS

#### Install awscli
- https://awscli.amazonaws.com/AWSCLIV2.pkg

#### Configure AWS
- https://console.aws.amazon.com/iam/home?region=ap-northeast-2#/users/fruit_developer?section=security_credentials
```bash
$ aws configure
AWS Access Key ID [None]: ****
AWS Secret Access Key [None]: ****
Default region name [None]: ap-northeast-2
Default output format [None]: json
```

#### Setup Virtualenv
```bash
$ python3 -m pip install virtualenv
$ git clone https://github.com/fruit-team/auth.git
$ cd auth/apple
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Test
```bash
$ brew install httpie
$ cd auth/apple
$ source venv/bin/activate
$ http $(chalice url)

```

### Deploy

```
$ cd auth/apple
$ source venv/bin/activate
$ chalice deploy --stage staging
```