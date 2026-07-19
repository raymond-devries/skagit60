import pulumi

from infra.get_django_aws import build_stack

STACK = pulumi.get_stack()

config = pulumi.Config()

aws_config = pulumi.Config("aws")
aws_region = aws_config.require("region")

extras = {"AWS_STORAGE_BUCKET_NAME": "skagit60-media"}

project_slug = "skagit60"
artifacts = build_stack(
    project_slug, None, extras, "lambda.Dockerfile"
)


