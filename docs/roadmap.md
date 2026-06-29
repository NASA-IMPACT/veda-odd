# ODD roadmap

This page exists to explain the motivations behind ODD's daily work. It connects what
we're building to why we're building it, and explains how work enters, moves through,
and may eventually leave our portfolio. The primary audience is the ODD team.
The secondary audience is peer ODSI teams who want to understand how our work fits the broader picture.

## Vision: who we serve

Our vision is expressed as the experiences users will have when we've succeeded:

1. **Ask in plain language and reproduce response.** As an Earth enthusiast, I want to ask questions like "how did the Gifford fire evolve?" and get an animated visual response — with links to the source code that produced the analysis, so I can verify and reproduce it.
2. **Explore in the browser.** As an Earth enthusiast, I want to visually explore forest disturbance through NISAR data directly in my browser, with no specialized software or cloud account.
3. **Research at scale.** As a fire event researcher, I want to evaluate relationships between variables from different data products across many thousands of fires, with minimal data pre-processing for fusion and modeling.
4. **Operate in near-real time.** As an operational **application**, I need products like HLS for disaster response or sea surface temperature for maritime operations available in near-real time.

## The gap

NASA already serves these users — but current services have limits that grow more acute as data volumes grow:

| User story                | Today's services                                   | Where they fall short                                                                                                                              |
| ------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ask in plain language     | Earth Information Explorer                         | Limited dataset access; datasets must be curated into the system                                                                                   |
| Explore in the browser    | Worldview / GIBS                                   | Not configurable by users; pre-rendered layers don't scale to new datasets or rendering needs                                                      |
| Research at scale         | Earthdata Cloud, Harmony, cloud-hosted JupyterHubs | Harmony offloads processing to servers — heavy compute cost rather than a structural fix; users struggle to find the best datasets for their needs |
| Operate in near-real time | LANCE + HLS                                        | Hard to keep metadata and data in sync; no reliable notification system for new data landing in Earthdata Cloud buckets                            |
| All of the above          | CMR                                                | Under increasing pressure from rapid archive growth and analytics-scale query traffic                                                              |

Across all of these: discovery is hard, and current systems are becoming unsustainable as data volumes grow.

## Our pillars

We address these gaps through four pillars:

1. **Open standards & FAIR data.** NASA data and services are findable, accessible, interoperable, and reusable, built on community standards rather than bespoke systems.
2. **Performance, cost & scale.** Optimize performance while minimizing cost, with solutions that scale sustainably to new and growing data volumes.
3. **Empowered users.** Users — both data providers and data consumers — can use and apply the solutions we build without us.
4. **Trusted & reliable data.** The data products NASA generates are verifiable, consistent, and kept in sync with their metadata.

**Cross-cutting foundation: community developed + adopted.** Every item on this roadmap is built in the open, with and for the community. Open source is the license; community development and adoption is the practice — it's how solutions outlive our involvement, and it underpins all four pillars.

## Roadmap

| Pillar                         | Now · mature                                                                      | Next · developing                                                                                                                 | Later · future                                                             |
| ------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Open standards & FAIR data** | ◆ Array format (Zarr) stewardship · ◆ Geospatial conventions (GeoZarr)            | Ecosystem sustainability · Codec re-architecture ·  variable chunking                                                             | Convention + CRS utilities                                                 |
| **Performance, cost & scale**  | Data virtualization · Object-store access · Dynamic tiling · In-browser rendering | Virtual stores + lazy array analytics · Analytics-scale metadata · Storage model evaluation                                       | Resampling/warp tooling · Query at scale · Storage cost optimization       |
| **Empowered users**            | Cloud-native guidance · Science support · Format evaluation                       | In-browser rendering · Cloud-optimized decision framework · Improved access & auth libraries · Dataset + tooling coverage metrics · AI/ML data-lake demonstrations | AI-assisted optimization (skills + tooling) · ESRI / ArcGIS integration    |
| **Trusted & reliable data**    | ◆ Transactional Zarr (Icechunk)                                                   | Remote store access · Live virtual stores · Synchronized metadata + data                                                          | Event-driven (object store notifications) for near-real time (NRT) updates |

**◆ Foundational** — a category of work that is ongoing. 

**Handed off:** nothing yet — see [How we work](#how-we-work). Building a working handoff path is a goal itself.

Every objective of this team should trace to at least one vision story and one pillar. Each item name links to deeper context below.

## Phases

While the grid above tracks *what* moves through our portfolio, the phases below sketch *when* — a notional sequence (timelines are notional, not concrete).

<svg viewBox="0 0 1200 380" width="100%" style="max-width:100%;height:auto;" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" role="img" aria-label="ODD phases notional timeline">
  <text x="20" y="26" font-size="18" font-weight="bold" fill="#0b2545">ODD phases — notional timeline</text>
  <text x="1180" y="26" font-size="12" fill="#64748b" text-anchor="end">timelines are notional, not concrete</text>
  <g fill="#475569" font-size="13" font-weight="bold" text-anchor="middle">
    <text x="152" y="56">FY26.4</text>
    <text x="376" y="56">FY27.1</text>
    <text x="600" y="56">FY27.2</text>
    <text x="824" y="56">FY27.3</text>
    <text x="1048" y="56">FY27.4</text>
  </g>
  <g stroke="#e2e8f0" stroke-width="1">
    <line x1="264" y1="64" x2="264" y2="250"/>
    <line x1="488" y1="64" x2="488" y2="250"/>
    <line x1="712" y1="64" x2="712" y2="250"/>
    <line x1="936" y1="64" x2="936" y2="250"/>
  </g>
  <line x1="40" y1="64" x2="40" y2="250" stroke="#cbd5e1"/>
  <line x1="1160" y1="64" x2="1160" y2="250" stroke="#cbd5e1"/>
  <rect x="40" y="80" width="448" height="48" rx="8" fill="#0e7490"/>
  <text x="60" y="109" font-size="14" font-weight="bold" fill="#ffffff">Demonstrate the data lake &#8212; varied datasets</text>
  <rect x="264" y="138" width="448" height="48" rx="8" fill="#0e7490"/>
  <text x="284" y="167" font-size="13.5" font-weight="bold" fill="#ffffff">Demonstrate the query engine + service integration</text>
  <rect x="712" y="196" width="448" height="48" rx="8" fill="#0e7490"/>
  <text x="732" y="225" font-size="14" font-weight="bold" fill="#ffffff">Demonstrate caching + AI use</text>
  <rect x="40" y="266" width="1120" height="46" rx="8" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="56" y="294" font-size="13" fill="#0f172a"><tspan font-weight="bold">Throughout: </tspan>socialization of the plan &#183; external-team integration &#183; iterating on the plan as we incorporate varied datasets</text>
  <rect x="40" y="322" width="1120" height="46" rx="8" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="56" y="350" font-size="13" fill="#0f172a"><tspan font-weight="bold">Foundational libraries: </tspan>Zarr &#183; Icechunk &#183; obstore (IO) &#183; warp / resampling / projection performance &#183; in-browser Zarr + COG &#183; GeoZarr &amp; standards</text>
</svg>

**FY26.4–27.1 — Demonstrate the data lake.** Demonstrate the utility and performance of Icechunk stores as a data lake platform across varied data types (HLS, NISAR, GPM IMERG, NLDAS, TEMPO, …). VEDA instances demonstrate the data lake in action with scientists, and we migrate the data services component (starting with TiTiler-CMR) to the Data Services team so ODD can prototype other services.

**FY27.1–27.2 — Demonstrate the query engine + service integration.** Show discovery and query across the lake via the query engine (DataFusion), and integrate it with the data services so a single interface serves discovery, query, and access.

**FY27.3–27.4 — Demonstrate caching + AI use.** Demonstrate caching performance using multiscales held in the Icechunk store and cached as a *data cache* (cached Zarr arrays), not a per-service tiling cache. Work with the AI/ML teams to demonstrate use of the data lake by AI (e.g. Water Insight or EIE): LLMs discover, reason about, and ingest data from the lake.

**Throughout — alongside every phase.** Socialization of the plan, integration of external teams, and iterating on the plan as we work to incorporate varied datasets. Plus continuation of foundational work in Zarr, Icechunk, and the underlying geospatial libraries: IO (obstore), warp / resampling / projection **performance**, reading and handling Zarr + COG directly in the browser, and geospatial data standards (GeoZarr).

## How we work

> "ODD should not be responsible for virtualizing everything! We (and our partners) are responsible for making it easy for NASA to virtualize things though." — Henry

ODD is a research and development team, not an operations or continued-maintenance team. Success for any item on this roadmap is *graduating off of it* — not staying on it indefinitely.

### Lifecycle

Work moves through four stages: **Later** (future, aspirational) → **Next** (developing) → **Now** (mature) → **Handed off** (owned by someone else).

An item is ready to hand off when it passes three tests:

1. **Someone else can do it.** Documentation, tooling, and skills exist so that a data provider or partner can reproduce the work without us.
2. **Someone else owns it.** A named owner — a DAAC, a mission team, community maintainers — has accepted responsibility.
3. **We've stopped learning.** Our remaining contribution is maintenance, not discovery.

Virtual data stores are an example: today we generate stores ourselves (learning). Next,
we will ship developer docs and optimization skills (enabling). Then store generation
graduates to data providers. Only the underlying tooling remains ours. Several
roadmap items — virtual store authoring docs, decision tooling, the optimization
skill/CLI, ecosystem sustainability (maintainer onboarding) — are not just projects but
handoff mechanisms.

We don't yet have a reliable handoff process. Naming that honestly is the first step; building it is on the roadmap.

### Prioritization

At each planning cycle (PI), we ask two questions of the grid:

- **What promotes?** Which Next items are ready to become Now? Which Later items are ready to become Next?
- **What graduates?** Which Now items pass the three handoff tests?

Objectives we take on must also balance "utopian" goals — like a unified Zarr model —
with the necessity of supporting legacy patterns and other formats.

When evaluating new candidate work, we apply these criteria:

- **Traceability.** Does it serve at least one vision story and one pillar?
- **Adoption readiness.** How quickly can the ecosystem absorb it? Building on familiar interfaces lowers the barrier (VirtualiZarr adopting xarray's data model made it immediately accessible); very new technology carries adoption lag as a risk (zarr-datafusion-search is powerful but the ecosystem may take years to take it on).
- **Cost.** What does adoption cost — in compute, energy, money, and user capability? Solutions that require cloud compute in a specific region, for example, exclude most users.
- **Handoff path.** Can we articulate who would eventually own this, even roughly?

## Deeper context

What each roadmap item unlocks, and what success looks like.

### Open standards & FAIR data

**◆ Array format stewardship.** The foundational format for cloud-native array data — Zarr. Ongoing maintenance and stewardship, including convening the community — e.g. Zarr Summit '26/27 — to unblock progress on technical features and convention adoption.

**◆ Geospatial conventions.** Zarr conventions for geospatial metadata (GeoZarr), essential for native and virtual Zarr collections to interoperate across GIS, visualization, and analysis libraries. Closing in on submission of the GeoZarr standard to the OGC architecture board. Success: trust and interoperability for Zarr data from all Earth data providers (NASA, NOAA, ESA), and a consistent, non-ambiguous platform to build client applications on.

**Ecosystem sustainability.** A sustainable maintainer ecosystem for Zarr to support growing, complex use cases — the zarr-python roadmap plus maintainer onboarding. Success: adoption of the roadmap by maintainers and stakeholders, plus one or two new onboarded maintainers making significant contributions — reducing stagnation and broadening design perspectives.

**Codec re-architecture.** The Zarr v2→v3 transition exposed design issues in the codec model. Re-architecting it supports new codec development (vital for virtualization, where archival formats use less-standardized codecs) and alternative client implementations in Rust and TypeScript. Follow-ons: *CF codecs* — capturing CF-convention decoding logic as codecs rather than attribute dictionaries, so clients interacting directly with the Zarr API don't need to duplicate xarray's specialized decoding logic; and *concatenated arrays* — supporting variable compression to unlock virtualization of quirky datasets like MUR SST (pre-design).

**Convention + CRS utilities.** Utilities and guidance for keeping virtual store metadata aligned with CF and GeoZarr conventions. Unblocks tools that rely on those conventions from using compliant virtual stores.

### Performance, cost & scale

**Data virtualization.** Access archival data through the Zarr API without duplicating it — VirtualiZarr. Includes parser improvements (virtual-tiff, obspec-utils, async-hdf5, GRIB) — or transitioning parser maintenance to partners, which is itself a handoff opportunity. This is also our current lever on storage cost (see *Storage cost optimization*).

**Object-store access.** High-performance object storage access for the Python geospatial stack — obstore.

**Dynamic tiling.** Tiling driven by CMR — TiTiler-CMR. Current work: regenerated compatibility report (with group support), OPERA integration into the disasters portal, a distributed cache for S3 credentials (~1s saved per cold-start request), and WMTS GetCapabilities so EGIS can surface HLS vegetation indices in ArcGIS.

**Lazy array analytics.** Instantly materialize massive lazy 4-D arrays (time, band, x, y) from metadata stores — lazycogs, a scalable replacement for stackstac/odc-stac. Success: any collection stored as COGs can be analyzed through a collection-level xarray API.

**Variable chunking.** Variable chunk support in VirtualiZarr + xarray; unlocks virtualizing more datasets. Near-term delivery.

**Analytics-scale metadata.** EOSDIS has identified pressure on CMR as a significant risk. Prototype collection-level stores using GeoParquet/Iceberg and zarr-datafusion to understand performance, cost, and scaling — and contribute to the relevant open-source libraries. Includes STAC in Iceberg: an object-storage-only STAC catalog giving providers API-less metadata access.

**Storage model evaluation.** Understand emerging storage models and their trade-offs — currently the S3 Files synchronization model: compare performance to native S3 for common operations and understand its pricing. Potential to serve both durable shared storage and the low-latency block access that ML and massively parallel array workloads need.

**Resampling/warp tooling.** A composable, Rust-based resampling/warp library reducing dependence on GDAL's monolithic toolchain. Usable from server-side tiling, distributed array frameworks (Dask, Cubed), and WASM in-browser rendering. Pre-design; builds on a full ecosystem assessment.

**Query at scale.** Query and access data at scale through a single interface — zarr-datafusion-search. Paves the way for Zarr as a storage target for Level 0/1 and swath data, and moves EOSDIS toward an Arrow-native ecosystem. High potential, but very new — adoption lag is the known risk.

**Storage cost optimization.** Addressing the growing cost of data volumes in Earthdata Cloud. We are not actively working on this beyond *data virtualization* (accessing archival data through the Zarr API without duplicating it). Avoiding duplication is the lever we pull today; broader storage cost strategies remain future work.

### Empowered users

**Cloud-native guidance.** The CNG guide: unblock people confused about which formats exist, why, and when to use each. Success: people use the guide to build cloud-native datasets, or to explain to stakeholders why a dataset was built a given way.

**Science support.** Direct support for science users, including cloud-optimized data usage guidance (e.g., xarray arguments) in the guide and datacube guide.

**Format evaluation.** Evaluate mission data formats and recommend improvements that enable optimized access patterns — currently NISAR: assess the NISAR HDF5 format and advise the Algorithm Development Team before the official release in summer 2026. Includes a virtualization + data fusion prototype showing a more user-friendly virtual representation.

**In-browser rendering.** In-browser GPU rendering of COGs and Zarr via direct data access (deck.gl-raster + Lonboard) — users customize rendering without re-fetching data. Current work: demonstrations in documentation (band combinations, direct access), initial GeoZarr support in both libraries, and a TypeScript WKB→GeoArrow parser enabling DuckDB-Wasm integration. Current limitation: requires open data access.

**Virtual store authoring.** How to build virtual stores, with or without agents — developer docs. Unblocks DAACs and science teams as virtual store developers — a primary handoff mechanism.

**Cloud-optimized decision framework.** The cloud-optimized data decision tree: a diagram plus explanatory text with examples per branch, guiding format and chunking decisions. Foundation for AI-assisted optimization.

**Improved access & auth libraries.** Libraries that get data and credentials into users' hands — earthaccess v1, notably a modular approach with refreshable credentials in a lightweight earth-auth package; finish opening Icechunk stores via earthaccess.

**AI-assisted optimization (skills + tooling).** A CLI and agentic skill for data structure optimization, plus an agent that walks data providers through chunking and format decisions (CO data AI guidance) — usable across ESDS. Builds on the cloud-optimized decision framework, reducing engineering time to a balanced or optimized data structure.

**Dataset + tooling coverage metrics.** Assess how many NASA datasets work with our tools (VirtualiZarr, datafusion, lazycogs) so we have metrics for improvement and impact.

**AI/ML data-lake demonstrations.** Data access is shifting from web / Python / in-house systems toward AI agents, making AI a primary class of user. Work with the AI/ML teams to demonstrate use of the data lake by AI — e.g. in Water Insight or EIE — in the first two quarters of FY27 (27.1–27.2). Show that LLMs can discover, reason about, and ingest data from the lake: semantic discovery beyond STAC, query via DataFusion, and direct Zarr ingest.

**ESRI / ArcGIS integration.** A large share of NASA data users work in ArcGIS, so our tools and data need to integrate with ESRI systems rather than require users to leave them. Ensure our cloud-native outputs are consumable there through the open standards ESRI already supports (COG, WMTS, OGC APIs, GeoZarr) — the EGIS/ArcGIS WMTS work in *Dynamic tiling* is the first concrete instance. Meeting users where they are, not requiring new software.

### Trusted & reliable data

**◆ Transactional Zarr.** Checksum verification and ACID transactions for Zarr stores (Icechunk) — the reliability layer.

**Remote store access.** Bearer-token HTTP support unblocks NASA data users without cloud compute in us-west-2 from using virtual stores — PO.DAAC has identified this as the single blocker to rolling out their Icechunk stores. Also: parsing manifests back out of Icechunk (inspection and modification of virtual stores, plus risk mitigation) and prefix-changing utilities.

**Live virtual stores.** Stores kept current as data lands — e.g. MUR SST as native Zarr, rechunked for time series, updated in near-real time as an AWS Public Dataset. Serves anyone doing historical or NRT sea surface temperature analysis, and demonstrates Icechunk's capabilities end to end.

**Synchronized metadata + data.** Keep metadata in sync with data (via zarr-datafusion-search) — addressing the gap where metadata and data drift apart.

**Event-driven NRT updates.** Icechunk makes all store updates trackable by listening to changes in object storage keys, enabling simple event-driven pipelines: dynamically updated pyramids (e.g., for Worldview), summary statistics, pre-computed time series. The path to keeping virtual stores current with incoming data streams — and to the near-real-time vision story.

---

*Open questions for the team: verify the Earth Information Explorer claim in the gap table; align timelines with data services (when do they stop coggifying?) and front-end teams (will tile servers eventually go away?); define our first formal handoff.*