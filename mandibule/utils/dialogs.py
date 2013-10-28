from mandibule.utils.i18n import _
from mandibule.utils.form import FormDialog, TextField, IntField, SelectField
from mandibule.config import CONFIG
import oerplib

def group_dialog(group=None):
    name = getattr(group, 'name', '')
    fields = (
            ('name', TextField(_("Name"), name)),
            )
    return FormDialog(fields).exec_()

def server_dialog(groups, server=None, group=None):
    name = getattr(server, 'name', '')
    if server:
        oerpd = oerplib.tools.session.get(server.name)
    else:
        oerpd = {}
    grps = {id(grp): grp for grp in groups}
    fields = (
            ('name', TextField(_("Name"), name)),
            ('group', SelectField(_("Group"),
                [(group_.name, id(group_)) for group_ in groups], id(group))),
            ('server', TextField(_("Host"), oerpd.get('server', ''))),
            ('port', IntField(_("Port"), oerpd.get('port', 8069),
                range_=(1, 65535))),
            ('database', TextField(_("Database"), oerpd.get('database', ''))),
            ('user', TextField(_("User"), oerpd.get('user', ''))),
            ('passwd', TextField(_("Password"), oerpd.get('passwd', ''))),
            )
    res, ok = FormDialog(fields).exec_()
    if ok:
        res['group'] = grps[res['group'][1]]
        res.update({'protocol': 'xmlrpc', 'timeout': 120, 'type': 'OERP'})
    return res, ok

