from mandibule.utils.form import FormDialog, TextField, IntField
from mandibule.utils.i18n import _

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
                'object',
                TextField(
                    _("Object"),
                    defaults.get('object', '')
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
    print 'Execute %s->%s' % (config.server.name, config.name)

