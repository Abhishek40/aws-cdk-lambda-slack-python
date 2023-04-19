from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
)
from constructs import Construct

class SlackCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        code_commit_lambda = _lambda.Function(self, "code-commit-state",
            code=_lambda.Code.from_asset("lambda_fun/codecommit_repo_state"),
            handler="codecommit_repo_state.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8
                                              )
        
        codeCommit_rule = _events.Rule(self, "code-commit-state-rule",
                event_pattern=_events.EventPattern(
                    source=["aws.codecommit"],
                    detail_type=["CodeCommit Repository State Change"]
                )
            )
        codeCommit_rule.add_target(_targets.LambdaFunction(code_commit_lambda))

        pipeline_state_lambda = _lambda.Function(self, "pipeline-state",
            code=_lambda.Code.from_asset("lambda_fun/pipeline_stage_change"),
            handler="pipeline_stage_change.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8)

        pipeline_state_rule = _events.Rule(self, "pipeline-state-rule",
                event_pattern=_events.EventPattern(
                    source=["aws.codepipeline"],
                    detail_type=["CodePipeline Stage Execution State Change"]
                    )
            )
        pipeline_state_rule.add_target(_targets.LambdaFunction(pipeline_state_lambda))

        trigger_pipeline_lambda = _lambda.Function(self, "trigger-pipeline",
            code=_lambda.Code.from_asset("lambda_fun/trigger_pipeline_slack"),
            handler="trigger_pipeline_slack.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8)
        
        trigger_pipeline_rule = _events.Rule(self, "trigger-pipeline-rule",
                event_pattern=_events.EventPattern(
                    source=["slack.devops"],
                    detail_type=["Execute our pipeline"]
                    )
            )
        
        trigger_pipeline_rule.add_target(_targets.CodePipeline(pipeline))