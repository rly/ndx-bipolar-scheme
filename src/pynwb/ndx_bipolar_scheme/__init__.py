import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_bipolar_scheme_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-bipolar-scheme.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_bipolar_scheme_specpath):
    ndx_bipolar_scheme_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-bipolar-scheme.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_bipolar_scheme_specpath)

EcephysExt = get_class('EcephysExt', 'ndx-bipolar-scheme')
