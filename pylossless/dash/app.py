from pathlib import Path
import dash

# loading raw object
from mne_bids import read_raw_bids, get_bids_path_from_fname
import mne

from pylossless.dash.qcgui import QCGUI


def get_test_assets(fname, ica_fpath, bads=(), verbose=False):
    bids_path = get_bids_path_from_fname(fname, verbose=verbose)
    raw = read_raw_bids(bids_path, verbose=False).pick('eeg')
    raw.info['bads'].extend(bads)

    ica = mne.preprocessing.read_ica(ica_fpath, verbose=verbose)
    info = mne.create_info(ica._ica_names,
                        sfreq=raw.info['sfreq'],
                        ch_types=['eeg'] * ica.n_components_, verbose=verbose)

    raw_ica = mne.io.RawArray(ica.get_sources(raw).get_data(), info, verbose=verbose)
    raw_ica.set_meas_date(raw.info['meas_date'])
    raw_ica.set_annotations(raw.annotations)

    return raw, raw_ica, ica


def get_app(assets_kwargs=None, kind="dash"):

    if assets_kwargs is None:
        assets_kwargs = {}
    if kind == "jupyter":
        from jupyter_dash import JupyterDash
        app = JupyterDash(__name__)

    else:
        app = dash.Dash(__name__)

    QCGUI(app, *get_test_assets(**assets_kwargs))
    return app    


if __name__ == '__main__':

    assets_kwargs = dict(fname=Path(__file__).parent / '../../assets/test_data/sub-s02/eeg/sub-s02_task-faceO_eeg.edf',
                         ica_fpath=Path(__file__).parent / '../../assets/test_data/sub-s02/eeg/sub-s02_task-faceO_ica2_ica.fif',
                         bads=('A27', 'A5', 'B10', 'B16', 'B17', 'B27', 'B28', 'C10', 'C17','C18', 'C3', 'D1'))
    get_app(assets_kwargs).run_server(debug=True, use_reloader=False)
