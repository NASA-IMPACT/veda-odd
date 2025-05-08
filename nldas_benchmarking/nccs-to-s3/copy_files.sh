# ssh -i ~/.ssh/abarciauskas.pem ec2-user@instance-ip

# write all nc files to a list file
timechunks="06"
export timechunks
export base_url="https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk${timechunks}/"

curl -s "https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk${timechunks}/" | \
  grep -oP '(?<=href=")[^"]+\.nc(?=")' > nc_files_${timechunks}.txt

# stream copying files
cat nc_files_${timechunks}.txt | parallel --ungroup -j 12 '
  echo "Transferring: {}" >&2
  rclone -P copyurl \
    "https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk${timechunks}/{}" \
    s3:nasa-eodc-scratch/NLDAS/netcdf/.timechunk${timechunks}/{}
'
