import xarray as xr
import pystac
from datetime import datetime

def create_stac_item(ds: xr.Dataset, url: str) -> pystac.Item:
    """Create a STAC item from an xarray Dataset."""
    # Get basic properties from the dataset
    properties = {
        "datetime": ds.time.values[0].astype(str) if 'time' in ds else None,
        "start_datetime": ds.time.values[0].astype(str) if 'time' in ds else None,
        "end_datetime": ds.time.values[-1].astype(str) if 'time' in ds else None,
    }
    
    # Add dataset attributes as properties
    if hasattr(ds, 'attrs'):
        properties.update(ds.attrs)
    
    # Extract bounding box and create geometry if lat/lon coordinates exist
    bbox = None
    geometry = None
    if 'lat' in ds.coords and 'lon' in ds.coords:
        west = float(ds.lon.min())
        south = float(ds.lat.min())
        east = float(ds.lon.max())
        north = float(ds.lat.max())
        
        bbox = [west, south, east, north]
        
        # Create a GeoJSON Polygon geometry from the bbox
        geometry = {
            "type": "Polygon",
            "coordinates": [[
                [west, south],  # southwest
                [east, south],  # southeast
                [east, north],  # northeast
                [west, north],  # northwest
                [west, south]   # close the polygon
            ]]
        }
    
    # Create the STAC item
    item = pystac.Item(
        id=f"nldas-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        geometry=geometry,
        bbox=bbox,
        datetime=datetime.fromisoformat(properties['datetime']) if properties['datetime'] else None,
        properties=properties
    )
    
    # Add the NetCDF file as an asset
    item.add_asset(
        "data",
        pystac.Asset(
            href=url,
            media_type="application/x-netcdf",
            roles=["data"]
        )
    )
    
    return item
