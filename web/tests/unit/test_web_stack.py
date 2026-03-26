import aws_cdk as core
import aws_cdk.assertions as assertions

from web.web_stack import WebStack

# example tests. To run these tests, uncomment this file along with the example
# resource in web/web_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WebStack(app, "web")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
