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

* time series generation for a single file, for 0.01, 1 and 5 spatial degrees squared.
* tile generation for a single timestep, for tiles at zoom 0, 4, and 8

### Libraries

For every operation, there are multiple libraries involved that greatly impact performance. These libraries integrate closely in order to deliver the desired result (some sort of data object). Generally these libraries make up the steps of:

* storage I/O | for timeseries: baseline: s3fs, others: obstore
* format-specific readers | baseline: h5netcdf/h5py, others: netcdf4
* data model or data representation | baseline: xarray, others: h5netcdf/h5py, netcdf4
* data operations such as averaging or resampling and reprojection | baseline: xarray (averaging for timeseries), rio_tiler (resampling + reprojection), others?


### Test datasets

We want to determine the impact of both chunk size and shape on time series and tile generation. Using the [01_rechunk/rechunk.ipynb notebook](./01_rechunk/rechunk.ipynb), we generated files with the following chunk shape configurations and resulting uncompressed chunk sizes:

| timesteps per chunk |  lat  |  lon  | Uncompressed Chunk Size (MB) |
|---------------------|-------|-------|-------------------------------|
|     24              |   50  |   90  | 0.41 MB                       |
|     24              |  100  |  180  | 1.65 MB                       |
|     24              |  500  |  900  | 41.18 MB                      |
|     24              | 1000  | 1800  | 164.73 MB                     |
|      6              |  100  |  180  | 0.41 MB                       |
|      6              |  200  |  360  | 1.65 MB                       |
|      6              | 1000  | 1800  | 41.18 MB                      |
|      6              | 2000  | 3600  | 164.73 MB                     |
|      1              |  250  |  450  | 0.43 MB                       |
|      1              |  500  |  900  | 1.65 MB                       |
|      1              | 2500  | 4500  | 41.18 MB                      |
|      1              | 5000  | 9000  | 164.73 MB                     |

Note: Only one daily file was used in these initial tests. Since there is currently not multi-file index, we expect performance to scale approximately linearly with number of files accessed when requests are made in sequence, and to be approximately the same when requests are made in parallel.

## Test Results

Time series results are detailed in [02_tests/timeseries_test.ipynb](./02_tests/timeseries_test.ipynb). Tile generation results are detailed in [02_tests/tiling_test.ipynb](./02_tests/tiling_test.ipynb).

The optimal chunking for time series generation is any option with 24 timesteps per chunk, whereas optimal chunking for tile generation are options where the most spatial coverage is included in each chunk, such as `{'time': 1, 'lat': 5000, 'lon': 9000}`. It is also notable that chunking configurations with small spatial coverage, such as `{'lat': 500, 'lon': 900}` and below, "time out" after the tile test limit of 60 seconds (arbitrarily selected).

**From these results it appears there is a clear tradeoff between optimizing for time series, which requries more data across the temporal dimension, and tiling, which requires more data across the spatial dimensions.**

We also know that the S3 byte range request size is configurable and can impact performance[^1]. A chunk size of 8-16MB is recommended. Note that while the uncompressed chunk size is important to consider for memory usage, the compressed chunk size is what matters for network performance. The compressed chunk size for each of the test files is plotted in [02_tests/chunk_sizes.ipynb](./02_tests/chunk_sizes.ipynb). A median compressed chunk size of 8-16MB appears to be associated with an uncompressed size of ~41MB.

Since the current S3FS default block size is 50MB, we additionally test the impact of changing the `default_block_size` in use by s3fs in [02_tests/timeseries_test-with-blocksize.ipynb](./02_tests/timeseries_test-with-blocksize.ipynb).

## Current Recommendations

The current recommendation would be a chunk shape of `{'time': 6, 'lat': 1000, 'lon': 1800}`, which has an uncompressed chunk size of 41.18MB. This is based on the byte range request size recommendations for S3 (8-16MB), the finding that this compressed chunk size is associated with the median compression size for a ~41MB uncompressed chunk size, and balancing the performance of time series with tile generation.

Also, when possible, S3 byte range request sizes should be closer aligned to the compressed chunk size. This recommendation is based on the principle that libraries can make the most efficient requests by aligning byte range requests with data blocks. In the [initial s3fs blocksize tests](./02_tests/timeseries_test-with-blocksize.ipynb)), it appears a smaller request block size results in better performance, however these results are highly contextual (i.e. dependent on the s3fs library and how its being used by xarray and h5netcdf).

# Future work

* **Additional performance tests:** Spatial differencing (see https://github.com/NASAWaterInsight/NLDAS-3/blob/develop/user_data_notebooks/3-temp_change_map.ipynb)
* **Library evaluations:** Evaluating the impact of caching in s3fs, xarray and h5netcdf libraries
* **Dataset Optimization:** Timeseries and tile generation using a virtual dataset, prepared with kerchunk or icechunk. Timeseries generation would be compared with


[1]: For small requests (<4MB) total duration is dominated by latency. For requests >8mb, throughput is bandwidth limited, so duration will increase proportionately to size. Source: [Exploiting Cloud Object Storage for High-Performance Analytics](https://www.vldb.org/pvldb/vol16/p2769-durner.pdf).
