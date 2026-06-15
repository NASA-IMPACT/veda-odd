# ODD roadmap

This page explains the motivations behind ODD's daily work. It connects what we're building to why we're building it. The primary audience is the ODD team. The secondary audience is peer ODSI teams who want to understand how our work fits the broader picture.

## Vision

If we are successful, we imagine users will be able to:

1. **Ask questions in plain language and reproduce the response:** As an Earth enthusiast, I want to ask questions like "how did the Gifford fire evolve?" and get an animated visual. I want to be able to reproduce responses with links to the source code that produced the analysis, so I can verify and reproduce it.
2. **Explore in the browser:** As an Earth enthusiast, I want to visually explore forest disturbance using NISAR data directly in my browser, with no specialized software or cloud account.
3. **Research at scale:** As a fire event researcher, I want to evaluate relationships between variables from different data products across many thousands of fires, with minimal data pre-processing for fusion and modeling.
4. **Operate in near-real time:** As an operational application, I need products like HLS for disaster response, or sea surface temperature for maritime operations, available in near-real time.

## The gap

NASA already serves these users — but current services have limits that grow more acute as data volumes grow:

| User story                | Today's services                                   | Where they fall short                                                                                                                              |
| ------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ask in plain language     | Earth Information Explorer                         | Limited dataset access; datasets must be curated into the system                                                                                   |
| Explore in the browser    | Worldview / GIBS                                   | Not configurable by users; pre-rendered layers don't scale to new datasets or rendering needs                                                      |
| Research at scale         | Earthdata Cloud, Harmony, cloud-hosted JupyterHubs | Harmony offloads processing to servers, requiring heavy compute cost; users struggle to find the best datasets for their needs |
| Operate in near-real time | LANCE + HLS                                        | Hard to keep metadata and data in sync; no reliable notification system for new data landing in Earthdata Cloud buckets                            |
| Data discovery         | CMR                                                | Under increasing pressure from rapid archive growth and analytics-scale query traffic                                                              |

## Our pillars

We address these gaps through four pillars:

1. **Open standards & FAIR data:** NASA data and services are findable, accessible, interoperable, and reusable, built on community standards rather than bespoke systems.
2. **Performance, cost & scale:** Optimize performance while minimizing cost, with solutions that scale sustainably to new and growing data volumes.
3. **Empowered users:** Users — both data providers and data consumers — can use and apply the solutions we build without us.
4. **Trusted & reliable data:** The data products NASA generates are verifiable, consistent, and kept in sync with their metadata.

Further, we maintain high standards for the software we develop or reuse, while never intending to duplicate effort. All software we develop or use should be of high quality, under an open source license, and developed and adopted by a broad community.

## Roadmap

Listed in the table below are technologies and technical components this team plans or is contributing to. We believe these components will make progress towards the vision and pillars described above.

Below, the **[Roadmap Items in Detail](#roadmap-items-in-detail) provides a brief description of each roadmap item.

* **Now · mature** means this is a mature technology. We are currently working on it but it is ready for adoption.
* **Next · developing** means this is a developing technology. We are currently working on it so it will be ready for adoption. Timeline for maturity and adoption readiness varies.
* **Later · future** means this is a technology we are not actively developing. We would like to work on it but other technologies in active development take precedence.

The **◆** designation represents a category of ongoing work. 

| Pillar                         | Now · mature | Next · developing| Later · future |
| ------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Open standards & FAIR data** | ◆ Array format (Zarr) stewardship · ◆ Geospatial conventions (GeoZarr) | Zarr Ecosystem sustainability · Codec re-architecture ·  variable chunking | Conventions + CRS utilities                                                 |
| **Performance, cost & scale**  | Data virtualization · Object-store access · Dynamic tiling · In-browser rendering | Virtual stores + lazy array analytics · Analytics-scale metadata · Storage model evaluation | Resampling/warp tooling · Query at scale · Storage cost optimization · Caching |
| **Empowered users** | Cloud-native guidance · Science support · Format evaluation | In-browser rendering · Cloud-optimized decision framework · Improved access & auth libraries · Dataset + tooling coverage metrics | AI-assisted optimization (skills + tooling) · ESRI / ArcGIS integration    |
| **Trusted & reliable data**  | ◆ Transactional Zarr (Icechunk) | Virtual stores for ongoing datasets · Synchronized metadata + data | Event-driven (object store notifications) for near-real time (NRT) updates |

## How we work

ODD is a research and development team, not an operations or continued-maintenance team. Success for any item on this roadmap is *graduating off of it* — not staying on it indefinitely.

### Lifecycle

Work moves through four stages: **Later** (future, aspirational) → **Next** (developing) → **Now** (mature) → **Handed off** (owned by someone else).

An item is ready to hand off when it passes three tests:

1. **Someone else can do it.** Documentation, tooling, and skills exist so that a data provider or partner can reproduce the work without us.
2. **Someone else owns it.** A named owner — a DAAC, a mission team, community maintainers — has accepted responsibility.
3. **We've stopped learning.** Our remaining contribution is maintenance, not discovery.

Virtual data stores are an example: today we generate stores ourselves (learning). Next,
we will ship developer docs and optimization skills (enabling). Then store generation
graduates to data providers. We would continue to work on underlying tooling. Several
roadmap items — documentation, decision tooling, the optimization
skill/CLI, ecosystem sustainability (maintainer onboarding) — are not just projects but
handoff mechanisms.

The above example is notional. We have not yet established a reliable handoff process. 

### Prioritization

Objectives we take on must also balance "utopian" goals — like a unified Zarr model —
with the necessity of supporting legacy patterns and other formats.

When evaluating new candidate work, we apply these criteria:

- **Traceability:** Does it serve at least one vision story and satisfy all appropriate pillars?
- **Adoption readiness:** How quickly can the ecosystem absorb it? Building on familiar interfaces lowers the barrier (VirtualiZarr adopting xarray's data model made it immediately accessible); very new technology carries adoption lag as a risk.
- **Cost:** What does adoption cost — in compute, energy, money, and user capability? Solutions that require cloud compute in a specific region, for example, exclude many users.
- **Handoff path:** Can we articulate who would eventually own this?

## Roadmap Items in Detail

Below, each technical component is briefly explained.

### Open standards & FAIR data

**◆ Array format stewardship:** The foundational format for cloud-native array data is Zarr. This component comprises ongoing maintenance and stewardship, including convening the community — e.g. Zarr Summit '26/27 — to unblock progress on technical features and convention adoption.

**◆ Geospatial conventions:** Zarr conventions for geospatial metadata (GeoZarr) are essential for native and virtual Zarr collections to interoperate across GIS, visualization, and analysis libraries. Success is trust and interoperability for Zarr data from all Earth data providers (NASA, NOAA, ESA), and a consistent platform to build client applications on.

**Ecosystem sustainability:** Zarr will support growing, complex use cases through a sustainable maintainer ecosystem. That ecosystem includes the work detailed in the zarr-python roadmap plus maintainer onboarding.

**Codec re-architecture:** The Zarr v2 -> v3 transition exposed design issues in the codec model. Re-architecting it supports new codec development (vital for virtualization, where archival formats use less-standardized codecs), alternative client implementations in Rust and TypeScript and fixing quirky data (CF codecs and concatenating arrays with varied codecs).

**Conventions + CRS utilities:** Utilities and guidance on CF and GeoZarr conventions will keep virtual store metadata aligned with tooling. This work will unblock tools that rely on those conventions from using compliant virtual stores.

### Performance, cost & scale

**Data virtualization:** Data virtualization enables access to archival data through the Zarr API without duplicating it. Work includes VirtualiZarr parser improvements (virtual-tiff, obspec-utils, async-hdf5, GRIB) and transitioning maintenance to partners.

**Object-store access:** Libraries such as obstore provide high-performance object storage access for the Python geospatial stack.

**Dynamic tiling:** Dynamic tiling enables visualization without maintaining static image pyramids. Future work includes supporting additional datasets and integrations, for example WMTS GetCapabilities so EGIS can surface HLS vegetation indices in ArcGIS.

**Lazy array analytics:** Instantly materialize massive lazy multi-dimensional arrays (time, band, x, y) from metadata stores, (e.g. lazycogs and lazymerge). These libraries provide a scalable replacement for stackstac/odc-stac.

**Variable chunking:** Variable chunk support in VirtualiZarr + xarray will unlock virtualizing more datasets.

**Analytics-scale metadata:** EOSDIS has identified pressure on CMR as a significant risk. We are prototype collection-level stores using GeoParquet/Iceberg and DataFusion to understand performance, cost, and scaling — and contribute to the relevant open-source libraries.

**Storage model evaluation:** We will evaluate emerging storage models and their trade-offs, such as the [S3 Files synchronization system](https://aws.amazon.com/s3/features/files/).

**Resampling/warp tooling.** A composable, Rust-based resampling/warp library will reduce dependence on GDAL's monolithic toolchain. Such a library would be useful for server-side tiling, distributed array frameworks (Dask, Cubed), and WASM in-browser rendering. This idea is stil in the design and ecosystem assessment phase.

**Query at scale:** We are demonstrating query and access data at scale through a single interface (zarr-datafusion-search). This library demonstrates a Zarr interface for Level 0/1 and swath data, and moves EOSDIS toward an Arrow-native ecosystem.

**Storage cost optimization:** Data virtualization addresses the growing cost of data volumes in Earthdata Cloud by accessing archival data through the Zarr API without duplicating it. Future work includes applying other storage cost strategies as evaluated in the work item listed above.

### Empowered users

**Cloud-native guidance:** The CNG guide unblocks people confused about which formats exist, why, and when to use each.

**Science support:** We continue to work with the dedicated science support team to provide cloud-optimized data guidance.

**Format evaluation:** We continue to evaulate mission data formats and recommend improvements that enable optimized access patterns. 

**In-browser rendering:** We are developing in-browser GPU rendering of COGs and Zarr via direct data access (e.g. deck.gl-raster + Lonboard). Users customize rendering without re-fetching data.

**Virtual store documentation:** Virtual store documentation (how to build virtual stores, with or without agents will unblock DAACs and science teams as virtual store developers.

**Cloud-optimized decision framework:** The cloud-optimized data decision tree will guide format and chunking decisions. This will also serve as the foundation for AI-assisted optimization.

**Improved access & auth libraries:** We provide development support to libraries that get data and credentials into users' hands (e.g. earthaccess).

**AI-assisted optimization (skills + tooling):** A CLI and agentic skill for data structure optimization will build on the cloud-optimized decision framework, reducing engineering time to a balanced or optimized data structure.

**Dataset + tooling coverage metrics:** An assessment of how many NASA datasets work with our tools (VirtualiZarr, datafusion, lazycogs) will provide metrics for improvement and impact.

**ESRI / ArcGIS integration:** A large share of NASA data users work in ArcGIS, so our tools and data need to integrate with ESRI systems. We need to ensure our cloud-native outputs are consumable there through the open standards ESRI already supports (COG, WMTS, OGC APIs, GeoZarr).

### Trusted & reliable data

**◆ Transactional Zarr:** Checksum verification and ACID transactions for Zarr stores, via Icechunk, provides reliability.

**Near-real time virtual stores:** We will keep stores current as data arrives. This work will serve anyone doing historical or NRT sea surface temperature analysis.

**Synchronized metadata + data:** Keep metadata in sync with data to ensure analysis are valid.

**Event-driven NRT updates:** Stores such as Icechunk make all store updates trackable by listening to changes in object storage keys. Simple event-driven pipelines will enable dynamically updated pyramids (e.g., for Worldview), summary statistics, and pre-computed time series. This is the path to keeping virtual stores current with incoming data streams.
