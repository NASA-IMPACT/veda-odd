# ssh -i ~/.ssh/abarciauskas.pem ec2-user@instance-ip

# write all nc files to a list file
export timechunks="01"
export base_url="https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk${timechunks}"

curl -s -L $base_url | grep -oP '(?<=href=")[^"]+\.nc(?=")' > nc_files_${timechunks}.txt
mkdir ncfiles

sudo yum install parallel -y
nohup bash -c "mkdir -p logs && cat nc_files_${timechunks}.txt | parallel --no-notice -j 4 'curl -L -o ncfiles/{} ${base_url}/{} 2>> logs/{}.log'" > output.log 2>&1 &

aws configure set default.s3.max_concurrent_requests 50
aws configure set default.s3.multipart_chunksize 64MB
nohup bash -c "aws s3 cp --recursive finished/ s3://nasa-eodc-scratch/NLDAS/netcdf/.timechunk${timechunks}/" > cp_to_s3_output.log 2>&1 &
