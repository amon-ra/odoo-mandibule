from mandibule.utils.form import FormDialog, TextField, IntField
from mandibule.utils.i18n import _

def new():
    print "relations new"
    return get_form().exec_()

def get_form(config=None):
    return FormDialog((
            (
                'name',
                TextField(
                    _("Name"),
                    getattr(config, 'name', '')
                    )
                ),
            (
                'object',
                TextField(
                    _("Object"),
                    getattr(config, 'object', '')
                    )
                ),
            (
                'maxdepth',
                IntField(
                    _("Max depth"),
                    getattr(config, 'maxdepth', 1),
                    range_=(1, 10)
                    )
                ),
            (
                'whitelist',
                TextField(
                    _("White list"),
                    getattr(config, 'whitelist', '')
                    )
                ),
            (
                'blacklist',
                TextField(
                    _("Black list"),
                    getattr(config, 'blacklist', '')
                    )
                ),
            (
                'attrs_whitelist',
                TextField(
                    _("Attrs white list"),
                    getattr(config, 'attrs_whitelist', '')
                    )
                ),
            (
                'attrs_blacklist',
                TextField(
                    _("Attrs black list"),
                    getattr(config, 'attrs_blacklist', '')
                    )
            ),
            ))



def execute():
    pass

