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
aws ec2 run-instances --image-id "ami-07b0c09aab6e66ee9" --instance-type "t3.medium" \
  --key-name "abarciauskas" \
  --network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-09774292ec4131f6f"]}' \
  --iam-instance-profile "Arn=arn:aws:iam::${ACCOUNT_ID}:instance-profile/ec2-s3-access-role" \
  --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"aimee-nldas-data-copy"}]}' \
  --user-data '#!/bin/bash
    # Install rclone
    curl https://rclone.org/install.sh | sudo bash

    # Setup config
    mkdir -p ~/.config/rclone
    cat <<"EOF" > ~/.config/rclone/rclone.conf
    [s3]
    type = s3
    provider = AWS
    env_auth = true
    region = us-west-2
    location_constraint = us-west-2
    acl = bucket-owner-full-control
    EOF

    export BASE_URL=https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk06
    export FILENAME=NLDAS_FOR0010_H.A20010110.030.beta.nc
    export URL=$BASE_URL/$FILENAME
    export timechunks="06"
    nohup bash -c "
      echo \"Transferring: \${URL}\" >&2
      rclone -P copyurl \"\${URL}\" \
      s3:nasa-eodc-scratch/NLDAS/netcdf/.timechunk\${timechunks}/filename.nc \
      --low-level-retries 10 \
      --retries 3 \
      --transfers 4 \
      --multi-thread-streams 4 \
      --buffer-size 32M \
      --timeout 2m \
      --contimeout 1m
    " > rclone_transfer.log 2>&1 &
  '
