from mandibule.controlers.group import GroupControler



class ServerListControler(object):
    """Main controler for serverlist widget"""
    def __init__(self, serverlist, parent):
        self.parent = parent
        self.widget = serverlist
        self.groups = {}
        for item in self.parent.data:
            self.add_group(item)

    def add_group(self, item):
        controler = GroupControler(self, item)
        self.widget.addTopLevelItem(controler.widget)
        self.groups[item['name']] = controler

    def remove_group(self, group):
        index = self.widget.indexOfTopLevelItem(group.widget)
        self.widget.TakeTopLevelItem(index)
        del self.groups[group.data['name']]


