from PySide import QtGui
from mandibule.utils.form import FormDialog, TextField, BoolField
from mandibule.utils.i18n import _
from mandibule.utils import zoomableimage
from mandibule.workarea import WorkAreaResultItem
import oerplib

def _clean(data):
    return [s.strip().encode('utf8') for s in data.split()]

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
                'modules',
                TextField(
                    _("Modules"),
                    defaults.get('modules', ''),
                    multi=True
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
    modules = _clean(config.data['modules'])
    models = _clean(config.data['models'])
    blacklist = _clean(config.data['blacklist'])
    oerp = oerplib.OERP.load(config.server.name)
    dependencies = oerp.inspect.dependencies(
            modules,
            models,
            blacklist,
            config.data['restrict'])
    graph = dependencies.make_dot().create_png()
    out = zoomableimage.ZoomableImage(graph)
    return WorkAreaResultItem(config.server.name, config.name, out)

