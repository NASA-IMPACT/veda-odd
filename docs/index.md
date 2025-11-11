# ODD Overview

Welcome to the documentation for the Optimized Data Delivery (ODD) team, working on the Visualization, Exploration and Data Analysis (VEDA) and Earth Observation Data on the Cloud (EODC) projects.

## ODD FY26 Roadmap

For a digest of what the team plans to work on this next year, please visit our [Fiscal Year (FY) 2026 Roadmap](./fy26-roadmap.md).


## TiTiler Ecosystem Documentation

We work extensively with the TiTiler ecosystem - a powerful suite of Python tools for creating dynamic tile servers from geospatial datasets. These docs should help familiarize new and existing team members with the titiler ecoysystem.

### What is TiTiler?

TiTiler is a FastAPI-based framework designed to create dynamic tile servers for geospatial data. It provides a modular architecture that enables efficient serving of map tiles from various data sources including Cloud Optimized GeoTIFFs (COGs and multi-dimensional scientific datasets.

### Quick Titiler Navigation

<div class="grid cards" markdown>

-   **🏗️ Ecosystem Overview**

    ---

    Learn about the components and architecture of the TiTiler ecosystem

    [:octicons-arrow-right-24: Explore Ecosystem](./titiler/ecosystem/overview.md)

-   **📚 API Reference**

    ---

    Interactive API documentation for all TiTiler applications

    [:octicons-arrow-right-24: API Documentation](./titiler/api/index.md)

</div>

### Key Titiler Features

- **Multi-format Support**: COGs, NetCDF, Zarr, and more
- **Dynamic Tiling**: On-demand tile generation with customizable rendering
- **Scientific Data**: Support for multi-dimensional datasets via the xarray extension
- **Performance Optimized**: Cloud-native design with caching and optimization strategies
- **Extensible Architecture**: Modular design enabling custom implementations
- **OGC Compliance**: Standards-compliant tile serving

---

*This documentation covers the TiTiler ecosystem tools and applications developed for dynamic geospatial data visualization and analysis.*
