# coding: utf-8
import h5py
import tempfile
import numpy as np

with tempfile.NamedTemporaryFile() as ntf:
    # Close the file so it can be re-opened by HDF5
    ntf.close()
    # Truncate the file
    f = h5py.File(ntf.name, mode="w")
    complevel = 9
    complib = "ztsd"
    shuffle = True
    data = np.random.random((1000, 1000))
    args = {
        "compression": 32015,
        "compression_opts": (),
    }
    print("compression args:", args)
    f.create_dataset("test_zstd", data=data, chunks=True, **args)
    f.close()
