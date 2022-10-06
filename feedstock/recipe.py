from pangeo_forge_recipes.patterns import ConcatDim, FilePattern
from pangeo_forge_recipes.recipes.xarray_zarr import XarrayZarrRecipe

# Sources:

# MPI, pers comms with Nils Brüggemann,
# links https://swiftbrowser.dkrz.de/public/dkrz_07387162e5cd4c81b1376bd7c648bb60/mpiom_fx/?show_all

# NCC: pers comms with Aleksi Nummelin
# link http://ns9560k.web.sigma2.no/inputdata/

url_dict = {
    "GFDL-ESM4": (
        "{mock_concat}ftp://ftp.gfdl.noaa.gov/"
        "perm/Alistair.Adcroft/MOM6-testing/OM4_05/ocean_hgrid.nc"
    ),
    "MPI-ESM1-2-HR": (
        "{mock_concat}https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/"
        "mpiom_fx/pool/data/MPIOM/input/r0013/GR15/GR15L40_fx.nc"
    ),
    "MPI-ESM1-2-LR": (
        "{mock_concat}https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/"
        "mpiom_fx/pool/data/MPIOM/input/r0013/TP04/TP04L40_fx.nc"
    ),
    "NorESM2-MM": (
        "{mock_concat}http://ns9560k.web.sigma2.no/inputdata/ocn/blom/grid/grid_tnx1v4_20170622.nc"
    ),  # testing if I need the mock_concat for http links
    "NorESM2-LM": (
        "{mock_concat}http://ns9560k.web.sigma2.no/inputdata/ocn/blom/grid/grid_tnx1v4_20170622.nc"
    ),
    "CNRM-CM6-1-HR": (
        "{mock_concat}https://filesender.renater.fr/download.php?token=dbb3014a-5a72-4bed-b011-551386676750&files_ids=14938340"
    "CESM2": (
        "{mock_concat}https://zenodo.org/record/6643449/files/CESM2_ocean_grid.nc?download=1"
    ),
    # "another_grid_key": (
    #   "{mock_concat}ftp://another_grid_source_file_url"
    # ),
}

time_concat_dim = ConcatDim("mock_concat", [""], nitems_per_file=1)

# Preprocessors
def gfdl_pp_func(ds, fname):
    return ds.drop("tile")  # dtype="|S255" is invalid for xarray

def CESM2_pp_func(ds, fname):
    return ds.drop(['moc_components', 'transport_components', 'transport_regions']) #ultimately it would be nice to have these uploaded to, but for now drop


preprocess_dict = {
    "GFDL-ESM4": gfdl_pp_func,
    "CESM2": CESM2_pp_func,
    # "another_grid_key": "another_grid_pp_func"
}

xr_open_kwargs_dict = {
    # "another_grid_key": "{xarray_open_kwargs for that grid_key}"
}

filepattern_kwargs_dict = {
    "GFDL-ESM4": {"file_type": "netcdf3"},
    "MPI-ESM1-2-HR": {"file_type": "netcdf3"},
    "MPI-ESM1-2-LR": {"file_type": "netcdf3"},
    "NorESM2-MM": {"file_type": "netcdf3"},
    "NorESM2-LM": {"file_type": "netcdf3"},
    # "another_grid_key": "{xarray_open_kwargs for that grid_key}"
}


def make_recipe(grid_key):

    def make_full_path(mock_concat):
        return url_dict[grid_key].format(mock_concat=mock_concat)

    pp = preprocess_dict.get(grid_key, None)
    xr_kwargs = xr_open_kwargs_dict.get(grid_key, {})
    fp_kwargs = filepattern_kwargs_dict.get(grid_key, {})

    filepattern = FilePattern(make_full_path, time_concat_dim, **fp_kwargs)

    return XarrayZarrRecipe(filepattern, process_input=pp, xarray_open_kwargs=xr_kwargs)


recipes = {k: make_recipe(k) for k in url_dict.keys()}
