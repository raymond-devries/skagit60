FROM public.ecr.aws/lambda/python:3.13

ARG MANAGEMENT=false

RUN if [ "$MANAGEMENT" = "true" ]; then \
    dnf install postgresql15 -y ; \
fi

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY tracker ${LAMBDA_TASK_ROOT}/tracker
COPY users ${LAMBDA_TASK_ROOT}/users
COPY skagit60 ${LAMBDA_TASK_ROOT}/skagit60
COPY static ${LAMBDA_TASK_ROOT}/static
COPY templates ${LAMBDA_TASK_ROOT}/templates
COPY infra/management_lambdas.py ${LAMBDA_TASK_ROOT}/infra/management_lambdas.py
