from mycroft import MycroftSkill, intent_file_handler


class Inventory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('inventory.intent')
    def handle_inventory(self, message):
        self.speak_dialog('inventory')


def create_skill():
    return Inventory()

