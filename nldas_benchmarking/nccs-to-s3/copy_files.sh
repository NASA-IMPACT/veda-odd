# ssh -i ~/.ssh/abarciauskas.pem ec2-user@instance-ip

# write all nc files to a list file
timechunks="06"
export timechunks
export base_url="https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk${timechunks}/"

curl -s $base_url | grep -oP '(?<=href=")[^"]+\.nc(?=")' > nc_files_${timechunks}.txt

# install and configure rclone
curl https://rclone.org/install.sh | sudo bash
rclone config # quit
cat <<EOF > ~/.config/rclone/rclone.conf
[s3]
type = s3
provider = AWS
env_auth = true
region = us-west-2
location_constraint = us-west-2
acl = bucket-owner-full-control
EOF

sudo yum install -y parallel

# stream copying files
nohup bash -c 'cat nc_files_${timechunks}.txt | parallel --ungroup -j 12 "
  echo \"Transferring: {}\" >&2
  rclone -P copyurl \
    \"${base_url}/{}\" \
    s3:nasa-eodc-scratch/NLDAS/netcdf/.timechunk${timechunks}/{}
"' > rclone_transfer.log 2>&1 &
