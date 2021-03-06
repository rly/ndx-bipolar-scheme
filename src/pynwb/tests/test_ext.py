import os
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTable, DynamicTableRegion
from datetime import datetime
from ndx_bipolar_scheme import EcephysExt
from pynwb.ecephys import ElectricalSeries

import numpy as np
from numpy.testing import assert_array_equal


def test_ext():
    nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

    device = nwbfile.create_device('device_name')

    electrode_group = nwbfile.create_electrode_group('electrode_group',
                                                     'desc', 'loc', device=device)

    for i in np.arange(20.):
        nwbfile.add_electrode(i, i, i, np.nan, 'loc', 'filt', electrode_group)

    bipolar_scheme = DynamicTable(name='bipolar_scheme', description='desc')
    bipolar_scheme.add_column(name='anode', description='desc', index=True, table=nwbfile.electrodes)
    bipolar_scheme.add_column(name='cathode', description='desc', index=True, table=nwbfile.electrodes)

    bipolar_scheme.add_row(anode=[0], cathode=[1])
    bipolar_scheme.add_row(anode=[0, 1], cathode=[2, 3])
    bipolar_scheme.add_row(anode=[0, 1], cathode=[2])

    ecephys_ext = EcephysExt(bipolar_scheme=bipolar_scheme)
    nwbfile.add_lab_meta_data(ecephys_ext)

    bipolar_scheme_region = DynamicTableRegion(
        name='electrodes',
        data=np.arange(0, 3),
        description='desc',
        table=nwbfile.lab_meta_data['extracellular_ephys_extensions'].bipolar_scheme)

    ec_series = ElectricalSeries(name='test_ec_series',
                                 description='desc',
                                 data=np.random.rand(100, 3),
                                 rate=1000.,
                                 electrodes=bipolar_scheme_region)

    nwbfile.add_acquisition(ec_series)

    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()
        assert_array_equal(nwbfile.acquisition['test_ec_series'].electrodes.table['anode'][2]['x'], [0., 1.])

    os.remove('test_nwb.nwb')
