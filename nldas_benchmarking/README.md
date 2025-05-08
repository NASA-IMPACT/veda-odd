# Benchmarking NLDAS chunking

## 1. In-progress: Copy files to S3 storage

Copy

https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk01/

https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk06/

https://portal.nccs.nasa.gov/lisdata_pub/NLDAS/.timechunk24/

to seperate directories s3://nasa-eodc-scratch/NLDAS/netcdf/.timechunk24/*.nc.

These are large files so we will use a virtual server with high network bandwidth.

See `nccs-to-s3` for scripts for setting up an ec2 instance and commands to copy the data.

## 2. In-progress: Create STAC metadata for indexing into those files

See `create_intake_stac` for in-progress work for creating a STAC catalog. Eventually we will save 3 intake-stac catalogs to s3://nasa-eodc-scratch/NLDAS/netcdf/.timechunkXX/intake.json.

## 3. Create virtual Zarr stores for each, using icechunk

Write virtual stores for each. s3://nasa-eodc-scratch/NLDAS/icechunk/.timechunkXX/

## 4. Define the test functions

Simplify and make arguments such as datetimes and bboxes programmatic. Ensure these test functions will work for both intake-stac (proxy for STAC) or virtualizarr.
https://github.com/NASAWaterInsight/NLDAS-3/blob/develop/user_data_notebooks/2-create_timeseries.ipynb
https://github.com/NASAWaterInsight/NLDAS-3/blob/develop/user_data_notebooks/3-temp_change_map.ipynb

These should be runnable as python scripts with datetimes and bboxes passed as arguments.

Running the python script should save results to a file.

## 5. Read the results

The results files should be readable with columns for dataset, temporal extent, spatial extent, test function and time to run.
