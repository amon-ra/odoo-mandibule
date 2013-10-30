#coding: utf8
from PySide import QtGui
from mandibule.utils.form import FormDialog, TextField, IntField
from mandibule.utils.i18n import _
from mandibule.workarea import WorkAreaResultItem
from mandibule.utils import zoomableimage
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
                'models',
                TextField(
                    _("Models"),
                    defaults.get('models', ''),
                    multi=True
                    )
                ),
            (
                'maxdepth',
                IntField(
                    _("Max depth"),
                    defaults.get('maxdepth', 1),
                    range_=(1, 10)
                    )
                ),
            (
                'whitelist',
                TextField(
                    _("White list"),
                    defaults.get('whitelist', ''),
                    multi=True
                    )
                ),
            (
                'blacklist',
                TextField(
                    _("Black list"),
                    defaults.get('blacklist', ''),
                    multi=True
                    )
                ),
            (
                'attrs_whitelist',
                TextField(
                    _("Attrs white list"),
                    defaults.get('attrs_whitelist', ''),
                    multi=True
                    )
                ),
            (
                'attrs_blacklist',
                TextField(
                    _("Attrs black list"),
                    defaults.get('attrs_blacklist', ''),
                    multi=True
                    )
            ),
            ))



def execute(config):
    models = _clean(config.data['models'])
    whitelist = _clean(config.data['whitelist'])
    blacklist = _clean(config.data['blacklist'])
    attrs_whitelist = _clean(config.data['attrs_whitelist'])
    attrs_blacklist = _clean(config.data['attrs_blacklist'])
    oerp = oerplib.OERP.load(config.server.name)
    relations = oerp.inspect.relations(
            models,
            config.data['maxdepth'],
            whitelist,
            blacklist,
            attrs_whitelist,
            attrs_blacklist)
    graph = relations.make_dot().create_png()
    out = zoomableimage.ZoomableImage(graph)
    return WorkAreaResultItem(config.server.name, config.name, out)
