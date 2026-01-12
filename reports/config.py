from datetime import date

# Manually maintained PI date ranges
# Update these when new PIs are planned
PI_DATES = {
    "pi-25.2": ("20250119", "20250418"),
    "pi-25.3": ("20250419", "20250718"),
    "pi-25.4": ("20250719", "20251018"),
    "pi-26.1": ("20251019", "20260117"),
    "pi-26.2": ("20260118", "20260425"),
}


def get_current_pi():
    """Find the current PI based on today's date."""
    today = date.today().strftime("%Y%m%d")
    for pi_name, (start, end) in PI_DATES.items():
        if start <= today <= end:
            return pi_name
    return None


def get_time_range(pi: str = None):
    """Get date range for a PI, or current PI if not specified."""
    if pi:
        return PI_DATES.get(pi)
    current = get_current_pi()
    if current:
        return PI_DATES[current]
    # Fallback to most recent PI if not in any range
    return list(PI_DATES.values())[-1]


TIME_RANGE = get_time_range()

# Quarterly objectives with repos and contributors per objective
# Run `uv run generate_config.py` to regenerate from GitHub issues
# - Objectives: Issues with pi-X.Y-objective labels
# - Contributors: Issue assignees
# - Repos: Labels matching repo:org/repo-name
OBJECTIVES = {
    "pi-25.2": [
        {
            "issue_number": 31,
            "title": "ODD PI 25.2 Objective 7: Increase data format support in VirtualiZarr",
            "state": "closed",
            "contributors": [
                ("Chuck Daniels", "chuckwondo"),
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 34,
            "title": "ODD PI 25.2 Objective 3: Visualize OCO-3 Datasets in VEDA",
            "state": "closed",
            "contributors": [
                ("Aimee Barciauskas", "abarciauskas-bgse"),
            ],
            "repos": [],
        },
        {
            "issue_number": 35,
            "title": "ODD PI 25.2 Objective 5: Deliver Virtual Zarr Stores for NASA Datasets Using Icechunk",
            "state": "closed",
            "contributors": [
                ("Aimee Barciauskas", "abarciauskas-bgse"),
            ],
            "repos": [],
        },
        {
            "issue_number": 36,
            "title": "ODD PI 25.2 Objective 6: Support for Modernizing VirtualiZarr to use zarr-python 3.0",
            "state": "closed",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Aimee Barciauskas", "abarciauskas-bgse"),
            ],
            "repos": [],
        },
        {
            "issue_number": 37,
            "title": "ODD PI 25.2 Objective 8: Support CMR Modernization",
            "state": "closed",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Kyle Barron", "kylebarron"),
            ],
            "repos": [],
        },
        {
            "issue_number": 40,
            "title": "ODD PI 25.2 Objective 1: Upgrade titiler and titiler-xarray to zarr-Python 3.0 and deploy to staging",
            "state": "closed",
            "contributors": [
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 41,
            "title": "ODD PI 25.2 Objective 4: Draft Web-Optimized Zarr (WOZ) Standard",
            "state": "closed",
            "contributors": [
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 76,
            "title": "ODD PI 25.2 Objective 2: Demonstrate how to tile HLS using titiler-cmr",
            "state": "closed",
            "contributors": [
                ("Henry Rodman", "hrodmn"),
            ],
            "repos": [],
        },
    ],
    "pi-25.3": [
        {
            "issue_number": 118,
            "title": "ODD PI 25.3 Objective 1: Support CMR Modernization",
            "state": "open",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Kyle Barron", "kylebarron"),
            ],
            "repos": [],
        },
        {
            "issue_number": 119,
            "title": "ODD PI 25.3 Objective 2: Continue to Build Out the VirtualiZarr Ecosystem",
            "state": "closed",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 124,
            "title": "ODD PI 25.3 Objective 3: Publish Cloud-Optimized Datasets",
            "state": "open",
            "contributors": [
                ("Chuck Daniels", "chuckwondo"),
                ("Aimee Barciauskas", "abarciauskas-bgse"),
            ],
            "repos": [],
        },
        {
            "issue_number": 126,
            "title": "ODD PI 25.3 Objective 4: Support TiTiler-CMR Adoption",
            "state": "closed",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Henry Rodman", "hrodmn"),
            ],
            "repos": [],
        },
        {
            "issue_number": 127,
            "title": "ODD PI 25.3 Objective 6: Community Involvement",
            "state": "closed",
            "contributors": [
                ("Max Jones", "maxrjones"),
                ("Aimee Barciauskas", "abarciauskas-bgse"),
                ("Henry Rodman", "hrodmn"),
            ],
            "repos": [],
        },
        {
            "issue_number": 165,
            "title": "ODD PI 25.3 Objective 5: Foundational Zarr-Python and Xarray Contributions",
            "state": "closed",
            "contributors": [
                ("Davis Bennett", "d-v-b"),
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
    ],
    "pi-25.4": [
        {
            "issue_number": 121,
            "title": "Potential ODD PI 25.4 Objective: Visualize Web-Optimized Zarr (WOZ) in VEDA (preview)",
            "state": "closed",
            "contributors": [
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 122,
            "title": "Potential 25.4 ODD Objective: Research, develop and document methods for Zarr and VirtualiZarr visualization",
            "state": "closed",
            "contributors": [
                ("Max Jones", "maxrjones"),
                ("Kyle Barron", "kylebarron"),
            ],
            "repos": [],
        },
        {
            "issue_number": 197,
            "title": "ODD PI 25.4 Objective 1: 🎬 TiTiler-CMR is production ready",
            "state": "open",
            "contributors": [
                ("Aimee Barciauskas", "abarciauskas-bgse"),
                ("Henry Rodman", "hrodmn"),
            ],
            "repos": [],
        },
        {
            "issue_number": 198,
            "title": "ODD PI 25.4 Objective 2: 🚀 Dataset support for VEDA instances",
            "state": "closed",
            "contributors": [
                ("Max Jones", "maxrjones"),
                ("Julius Busecke", "jbusecke"),
            ],
            "repos": [],
        },
        {
            "issue_number": 203,
            "title": "ODD PI 25.4 Objective 3: 🗺️Research, develop and document methods for Zarr and VirtualiZarr data services",
            "state": "open",
            "contributors": [
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 204,
            "title": "ODD PI 25.4 Objective 4: 🛠️ Zarr Development",
            "state": "open",
            "contributors": [
                ("Davis Bennett", "d-v-b"),
                ("Max Jones", "maxrjones"),
            ],
            "repos": [],
        },
        {
            "issue_number": 205,
            "title": "ODD PI 25.4 Objective 5: 🤗 Community engagement",
            "state": "closed",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Chuck Daniels", "chuckwondo"),
                ("Max Jones", "maxrjones"),
                ("Aimee Barciauskas", "abarciauskas-bgse"),
            ],
            "repos": [],
        },
        {
            "issue_number": 206,
            "title": "ODD PI 25.4 Objective 6: 📦 Obstore outreach",
            "state": "closed",
            "contributors": [
                ("Chuck Daniels", "chuckwondo"),
                ("Kyle Barron", "kylebarron"),
            ],
            "repos": [],
        },
    ],
    "pi-26.1": [
        {
            "issue_number": 244,
            "title": "ODD PI 26.1 Objective 1: 🗺️ Add dynamic tiling and timeseries support for Virtual Zarr Stores",
            "state": "open",
            "contributors": [
                ("Julius Busecke", "jbusecke"),
                ("Henry Rodman", "hrodmn"),
            ],
            "repos": [
                ("developmentseed", "titiler"),
                ("earth-mover", "icechunk"),
            ],
        },
        {
            "issue_number": 245,
            "title": "ODD PI 26.1 Objective 2: 🌍 Add dynamic tiling and timeseries support for datasets in CMR",
            "state": "open",
            "contributors": [
                ("Aimee Barciauskas", "abarciauskas-bgse"),
                ("Henry Rodman", "hrodmn"),
            ],
            "repos": [
                ("developmentseed", "titiler"),
                ("developmentseed", "titiler-cmr"),
                ("developmentseed", "titiler-lambda-layer"),
                ("developmentseed", "titiler-md-demo"),
                ("nasa", "python_cmr"),
            ],
        },
        {
            "issue_number": 246,
            "title": "ODD PI 26.1 Objective 3: 🤖 Support virtualization of additional data products",
            "state": "open",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Max Jones", "maxrjones"),
                ("Julius Busecke", "jbusecke"),
            ],
            "repos": [
                ("zarr-developers", "virtualizarr"),
                ("virtual-zarr", "obspec-utils"),
                ("virtual-zarr", "virtual-tiff"),
                ("virtual-zarr", "hrrr-parser"),
                ("developmentseed", "async-tiff"),
                ("developmentseed", "virtualizarr-data-pipelines"),
                ("earth-mover", "icechunk"),
            ],
        },
        {
            "issue_number": 247,
            "title": "ODD PI 26.1 Objective 4: 🛰 Explore scalable, cloud native approaches for search, discovery and access of non-gridded data",
            "state": "closed",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Kyle Barron", "kylebarron"),
            ],
            "repos": [
                ("developmentseed", "obstore"),
                ("developmentseed", "obspec"),
                ("developmentseed", "zarr-datafusion-search"),
                ("geoarrow", "geoarrow-rs"),
                ("datafusion-contrib", "arrow-zarr"),
            ],
        },
        {
            "issue_number": 248,
            "title": "ODD PI 26.1 Objective 5: 🤗 Support community adoption of the technologies incubated by EODC and VEDA",
            "state": "open",
            "contributors": [
                ("Sean Harkins", "sharkinsspatial"),
                ("Chuck Daniels", "chuckwondo"),
                ("Max Jones", "maxrjones"),
                ("Aimee Barciauskas", "abarciauskas-bgse"),
            ],
            "repos": [
                ("zarr-developers", "geozarr-spec"),
                ("zarr-developers", "zarr-python"),
                ("zarr-conventions", "multiscales"),
                ("zarr-conventions", "geo-proj"),
                ("zarr-conventions", "spatial"),
                ("developmentseed", "datacube-guide"),
                ("developmentseed", "geozarr-examples"),
                ("developmentseed", "warp-resample-profiling"),
                ("pangeo-data", "pangeo.io"),
                ("pangeo-data", "pangeo-docker-images"),
                ("nasa-openscapes", "earthdata-cloud-cookbook"),
            ],
        },
    ],
}


def get_all_repos():
    """Derive unique repos from all objectives."""
    repos = set()
    for pi_objectives in OBJECTIVES.values():
        for obj in pi_objectives:
            for repo in obj["repos"]:
                repos.add(repo)
    return sorted(repos)


def get_all_contributors():
    """Derive unique contributors from all objectives."""
    contributors = {}
    for pi_objectives in OBJECTIVES.values():
        for obj in pi_objectives:
            for name, username in obj["contributors"]:
                contributors[username] = name
    return [
        (name, username)
        for username, name in sorted(contributors.items(), key=lambda x: x[1])
    ]


def get_repos_for_pi(pi: str):
    """Get all repos for a specific PI."""
    repos = set()
    for obj in OBJECTIVES.get(pi, []):
        for repo in obj["repos"]:
            repos.add(repo)
    return sorted(repos)


def get_contributors_for_pi(pi: str):
    """Get all contributors for a specific PI."""
    contributors = {}
    for obj in OBJECTIVES.get(pi, []):
        for name, username in obj["contributors"]:
            contributors[username] = name
    return [
        (name, username)
        for username, name in sorted(contributors.items(), key=lambda x: x[1])
    ]
