import h5py
import pygrib

def grib_to_hdf5(grib_file_path, hdf5_file_path):
    grbs = pygrib.open(grib_file_path)

    # Create HDF5 file
    with h5py.File(hdf5_file_path, 'w') as h5f:
        # Loop over all messages in the GRIB file
        for grb in grbs:
            # We are only interested in 'Total precipitation'
            if grb.name == 'Total precipitation':
                # Create a unique name for each dataset - you can customize this
                dataset_name = f"{grb.name.replace(' ', '_')}_{grb.forecastTime}"
                # Get data array
                data, lats, lons = grb.data()
                # Create a group for this dataset
                grp = h5f.create_group(dataset_name)
                # Create datasets for data, lats, lons
                grp.create_dataset('data', data=data)
                grp.create_dataset('lats', data=lats)
                grp.create_dataset('lons', data=lons)
                # Store metadata as attributes
                for key in grb.keys():
                    if isinstance(grb[key], (int, float, str)):
                        grp.attrs[key] = grb[key]

grib_to_hdf5('input.grib2', 'output.hdf5')