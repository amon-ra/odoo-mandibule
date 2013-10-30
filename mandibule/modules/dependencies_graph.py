from PySide import QtGui
from mandibule.utils.form import FormDialog, TextField, BoolField
from mandibule.utils.i18n import _
from mandibule.utils import zoomableimage
from mandibule.workarea import WorkAreaResultItem
#import oerplib

def get_form(config=None):
    defaults = getattr(config, 'data', {})
    return FormDialog((
            (
                'name',
                TextField(
                    _("Name"),
                    defaults.get('name', '')
                    )
                ),
            (
                'models',
                TextField(
                    _("Models"),
                    defaults.get('models', ''),
                    multi=True
                    )
                ),
            (
                'blacklist',
                TextField(
                    _("Blacklist"),
                    defaults.get('blacklist', ''),
                    multi=True
                    )
                ),
            (
                'restrict',
                BoolField(
                    _("Restrict"),
                    defaults.get('restrict', False)
                    )
                )
            ))


def execute(config):
    with open('/home/fred/test.png') as fp:
        img = zoomableimage.ZoomableImage(fp.read())
        return WorkAreaResultItem('test', 'test', img)

    '''
    oerp = oerplib.load(config.server.name)
    return (config.server.name, config.name, widget)
    '''

