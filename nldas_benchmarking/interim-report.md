# North American Land Data Assimilation System (NLDAS) Benchmarking Interim Report

## Goal

Support determination of a chunk size selection for the NLDAS Forcing dataset which may inform future datasets.

## Background

### Dataset

The North American Land Data Assimilation System (NLDAS) project produces multiple datasets, detailed in tables on [this NLDAS-3 information page](https://ldas.gsfc.nasa.gov/nldas/v3). The one tested in this report is the surface forcings documented in Table 1. This data product is produced as daily NetCDF files with:

* 8 variables of data type `float32`
* 24 timesteps per file (i.e. hourly timesteps)
* 0.01 degree spatial resolution over the North American region (-169 to -59 degrees longitude, 7 to 72 degrees latitude)

### AWS Object Storage (S3)

Cloud-based data storage and distribution is most commonly implemented using cloud object storage. Cloud object storage provides nearly infinite scalability of both reading and writing, making it an attractive option to store and make available large volumes of data for a wide variety of applications.

All major cloud providers offer a cloud object storage solution with varying performance characteristics. NASA's Earthdata System has decided on Amazon Web Service's (AWS) Simple Storage Solution (S3), so we will focus our attention on recommendations suitable for storage and retrieval on AWS S3.

The following recommendations for storing and retrieving data from S3 should be taken into consideration:
* A minimum latency of 100ms [Best practices design patterns: optimizing Amazon S3 performance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)
* Use byte-range fetches, with a recommended request size of 8-16MB[^1]. To maximize throughput, use concurrent connections to saturate the network. AWS suggests 1 concurrent request per 85-90 MB/s desired throughput. Source: [Performance design patterns for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-parallelization).


## Methodology

To achieve the goal of recommending a chunk size and shape for the NLDAS-3 data, we first determine what types of operations to optimize for. For what operations to optimize for, we refer to the [user notebooks](https://github.com/NASAWaterInsight/NLDAS-3/tree/develop/user_data_notebooks). We also know this dataset may be visualized in a VEDA dashboard. For our initial tests we include:

### Initial tests

* time series generation for a single file, for 0.01, 1 and 5 spatial degrees squared.
* tile generation for a single timestep, for tiles at zoom 0, 4, and 8

### Libraries

For every operation, there are multiple libraries involved that greatly impact performance. These libraries integrate closely in order to deliver the desired result (some sort of data object). Generally these libraries make up the steps of:

* storage I/O | for timeseries: baseline: s3fs, others: obstore
* format-specific readers | baseline: h5netcdf/h5py, others: netcdf4
* data model or data representation | baseline: xarray, others: h5netcdf/h5py, netcdf4
* data operations such as averaging or resampling and reprojection | baseline: xarray (averaging for timeseries), rio_tiler (resampling + reprojection), others?


### Test datasets

We want to determine the impact of both chunk size and shape on time series and tile generation.

[ADD ME]

## Test Results

## Current Recommendations

# Future work

Additional performance tests:
* Spatial differencing (see https://github.com/NASAWaterInsight/NLDAS-3/blob/develop/user_data_notebooks/3-temp_change_map.ipynb)

Evaluate libraries
* Evaluating the impact of caching in s3fs, xarray and h5netcdf libraries
* Evaluating the impact of changing the s3fs blocksize (research if xarray/s3fs/h5netcdf are optimizing)

Dataset Optimization:
* Timeseries and tile generation using a virtual dataset, prepared with kerchunk or icechunk


[1]: For small requests (<4MB) total duration is dominated by latency. For requests >8mb, throughput is bandwidth limited, so duration will increase proportionately to size. Source: [Exploiting Cloud Object Storage for High-Performance Analytics](https://www.vldb.org/pvldb/vol16/p2769-durner.pdf).
