from aws_cdk import (
    Duration,
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_lambda as _lambda
)
from constructs import Construct


class ComplianceLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Lambda function
        compliance_lambda = _lambda.Function(
            self,
            'ComplianceLambda',
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset('lambda'),
            handler='index.lambda_handler',
            description='Turns on detailed monitoring on EC2 instances'
        )

        # Add permission to call DescribeInstances and MonitorInstances
        compliance_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    'ec2:DescribeInstances',
                    'ec2:MonitorInstances',
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        # Eventbridge rule to call the Lambda function every day
        events.Rule(
            self,
            'Rule',
            description='Turns on detailed monitoring on EC2 instances',
            schedule=events.Schedule.rate(Duration.days(1)),
            targets=[targets.LambdaFunction(compliance_lambda)]
        )
