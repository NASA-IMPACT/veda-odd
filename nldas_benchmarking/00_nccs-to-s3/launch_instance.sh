## List network performance of diffent instance types
# aws ec2 describe-instance-types \
#     --filters "Name=instance-type,Values=r5*" \
#     --query "InstanceTypes[].[InstanceType, NetworkInfo.NetworkPerformance, NetworkInfo.NetworkCards[0].BaselineBandwidthInGbps] | sort_by(@,&[2])" \
#     --output table

## Create a security group - don't need to do this more than once
# MYIP=XXX
# VPCID=XXX
# aws ec2 create-security-group --group-name "launch-wizard-8" --description "launch-wizard-8 created 2025-05-08T15:04:34.591Z" --vpc-id $VPCID
# aws ec2 authorize-security-group-ingress --group-id "sg-preview-1" --ip-permissions '{"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"$MYIP"}]}'

export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ec2 run-instances --image-id "ami-07b0c09aab6e66ee9" --instance-type "t3.xlarge" \
  --key-name "abarciauskas" \
  --network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-09774292ec4131f6f"]}' \
  --iam-instance-profile "Arn=arn:aws:iam::${ACCOUNT_ID}:instance-profile/ec2-s3-access-role" \
  --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"aimee-nldas-data-copy"}]}' \
  --block-device-mappings '[{
    "DeviceName": "/dev/xvda",
    "Ebs": {
      "VolumeSize": 200,
      "VolumeType": "gp3",
      "DeleteOnTermination": true
    }
  }]' \
  --count 1  
