---
name: aws-sam
description: "Conventions for AWS SAM templates (Python and Node.js runtimes). Use when: authoring or reviewing SAM template.yaml files, adding Lambda functions, configuring API Gateway, setting up CloudWatch log groups, or deploying serverless stacks."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# AWS SAM Skill

Use these conventions when authoring AWS SAM templates in this codebase. Apply these rules whenever creating or reviewing `template.yaml` files.

## Architecture

Always use `x86_64`. Do not use `arm64`.

```yaml
Globals:
  Function:
    Architectures:
      - x86_64
```

## Log Groups — Create Manually for All Resources

**Always create `AWS::Logs::LogGroup` resources explicitly** for every resource that writes logs. This is the only way to set a retention policy. Never rely on auto-created log groups.

### Lambda Log Groups

Create the log group before the Lambda function. Use `DependsOn` to enforce the order.

```yaml
  MyFunctionLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub /aws/lambda/my-function-${Environment}
      RetentionInDays: 30

  MyFunction:
    Type: AWS::Serverless::Function
    DependsOn: MyFunctionLogGroup
    Properties:
      FunctionName: !Sub my-function-${Environment}
      ...
```

### API Gateway — Access Log Group

The access log group name is a free-form string. Create the log group manually. Reference it in `AccessLogSetting`.

```yaml
  MyApiAccessLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub /aws/apigateway/my-api-access-${Environment}
      RetentionInDays: 30

  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      AccessLogSetting:
        DestinationArn: !GetAtt MyApiAccessLogGroup.Arn
        Format: '{"requestId":"$context.requestId","ip":"$context.identity.sourceIp","requestTime":"$context.requestTime","httpMethod":"$context.httpMethod","path":"$context.path","status":"$context.status","protocol":"$context.protocol","responseLength":"$context.responseLength"}'
```

### API Gateway — Execution Log Group

AWS fixes the execution log group name: `API-Gateway-Execution-Logs_{rest-api-id}/{stage}`. Create it with `DependsOn: MyApi`. The log group name requires the API's physical ID. Create the API first. This dependency is unavoidable and acceptable.

```yaml
  MyApiExecutionLogGroup:
    Type: AWS::Logs::LogGroup
    DependsOn: MyApi
    Properties:
      LogGroupName: !Sub "API-Gateway-Execution-Logs_${MyApi}/${Environment}"
      RetentionInDays: 30
```

### Log Group Summary Checklist

| Resource | Log Group Name Pattern | DependsOn |
|---|---|---|
| Lambda | `/aws/lambda/<function-name>-${Environment}` | Lambda `DependsOn` log group |
| API GW access | Any descriptive name | None |
| API GW execution | `API-Gateway-Execution-Logs_${MyApi}/${Environment}` | Log group `DependsOn` API |

## Node.js Runtime

Use `npm run build` to compile TypeScript with `tsc`. Do **not** use esbuild.

- Run `npm run build` in CI before `sam build`.
- The `tsc` output goes to `dist/` (e.g. `dist/handlers/health.js`).
- Set `Handler` to reflect the `dist/` outDir: `dist/handlers/health.handler`.
- Set `CodeUri: .` to point SAM at the package root (`src-node/`). SAM runs `npm install --production`. SAM then uses the pre-compiled `dist/` files.

```yaml
  MyNodeFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: nodejs24.x
      CodeUri: .
      Handler: dist/handlers/myhandler.handler
```

CI step order:
1. `npm ci`
2. `npm run build`   ← tsc compile
3. `sam build`
4. `sam deploy`

## Python Runtime

- Set `CodeUri: .` to point SAM at `src-python/`.
- SAM installs dependencies from `src-python/requirements.txt`.
- Set the handler path relative to `src-python/`: `handlers/backend.handler`.

```yaml
  MyPythonFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.14
      CodeUri: .
      Handler: handlers/backend.handler
```

## API Gateway Type

Use REST API (`AWS::Serverless::Api`), not HTTP API. REST API is required for Lambda response streaming support.

```yaml
Globals:
  Api:
    EndpointConfiguration: REGIONAL
```

## Cross-Stack Handoff via SSM

Publish Lambda ARNs and Terraform-owned resource references through SSM Parameter Store. Use CloudFormation dynamic references to consume them.

```yaml
# Publish
  BackendLambdaArnParameter:
    Type: AWS::SSM::Parameter
    Properties:
      Name: !Sub /myapp/backend-lambda-arn
      Type: String
      Value: !GetAtt MyFunction.Arn

# Consume in another stack
  BACKEND_LAMBDA_ARN: !Sub "{{resolve:ssm:/myapp/backend-lambda-arn}}"
```

## IAM Policy — CloudWatch Logs

The Lambda role still needs stream and event permissions when you create the Lambda log group manually. The role does not need `CreateLogGroup` because the group already exists. Scoping `CreateLogGroup` to `Resource: "*"` is harmless and avoids deploy-order sensitivity.

```yaml
- Sid: CloudWatchLogsAccess
  Effect: Allow
  Action:
    - logs:CreateLogStream
    - logs:PutLogEvents
  Resource: !Sub arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/my-function-${Environment}:*
```

## Required Tags

Apply the required tags through `Globals.Function.Tags`:

```yaml
Globals:
  Function:
    Tags:
      Environment: !Ref Environment
      Application: <app-name>
      ManagedBy: sam
```
