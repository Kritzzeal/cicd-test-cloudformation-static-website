from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origin,
    aws_s3_deployment as s3_deploy,
    RemovalPolicy,
    CfnOutput
    # aws_sqs as sqs,
)
from constructs import Construct
import os
class WebStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        web_bucket = s3.Bucket(self, "WebBucket",
            bucket_name="web-bucket-1234567890890456689568789vnkgbkgb",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        ui_dir=os.path.join(os.path.dirname(__file__),"..","..","static-web","dist")
        
        if not os.path.exists(ui_dir):
            raise Exception(f"UI directory {ui_dir} does not exist. Please build the UI first.")
            return
        
        origin_permissions=cloudfront.OriginAccessIdentity(self, "WebOriginAccessIdentity")
        web_bucket.grant_read(origin_permissions)
        web_cloudfront = cloudfront.Distribution(self, "WebCloudFront",
                    default_root_object="index.html",
                    default_behavior=cloudfront.BehaviorOptions(
                        origin=origin.S3Origin(
                            web_bucket,origin_access_identity=origin_permissions
                        )
                    ),
                )
                    
        s3_deploy.BucketDeployment(self,"WebBucketDeployment",
                                sources=[s3_deploy.Source.asset(ui_dir)],
                                destination_bucket=web_bucket,
                                distribution=web_cloudfront,
                                )          
                    
        CfnOutput(self,"Url",value=web_cloudfront.distribution_domain_name)
            