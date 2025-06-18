FROM public.ecr.aws/lambda/python:3.11

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY main.py ${LAMBDA_TASK_ROOT}
COPY processor.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["main.lambda_handler"] 