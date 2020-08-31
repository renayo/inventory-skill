import csv
import shutil
from os.path import dirname, join
from mycroft import MycroftSkill, intent_file_handler

inventoryfile = join(dirname(__file__), 'inventory.txt')
editfile = join(dirname(__file__), 'edit.txt')

class Inventory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
                                      
        def initialize(self):
            self.register_intent_file('inventory start.intent', self.handle_inventorystart)
            self.register_intent_file('inventory read.intent', self.handle_inventoryread)
            self.register_intent_file('inventory where.intent', self.handle_inventorywhereis)
            self.register_intent_file('inventory what.intent', self.handle_inventorywhatis)
            self.register_intent_file('inventory remove.intent', self.handle_inventoryremove)
            self.register_intent_file('inventory add.intent', self.handle_inventoryadd)
            self.register_intent_file('inventory move.intent', self.handle_inventorymove)
            
    @intent_file_handler('inventory start.intent')
    def handle_inventorystart(self, message):
        self.speak_dialog('inventory start')

    @intent_file_handler('inventory read.intent')
    def handle_inventoryread(self, message):
        self.speak_dialog('inventory read')
        with open(inventoryfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                linemessage=f'{row[0]} resides in {row[1]}.'
                self.speak(linemessage)

    @intent_file_handler('inventory where.intent')
    def handle_inventorywhereis(self, message):
        self.obj = message.data.get('obj')
        with open(inventoryfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == self.obj:
                    linemessage = self.obj+ ' resides in '+row[1]
                    self.speak(linemessage)
                    
    @intent_file_handler('inventory what.intent')
    def handle_inventorywhatis(self, message):
        self.loc = message.data.get('loc');
        locationlist=[];
        s = ', '
        with open(inventoryfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[1] == self.loc:
                    locationlist.append(row[0])
            if len(locationlist) > 0:
                linemessage = self.loc+ ' contains ' + s.join(locationlist)
                self.speak(linemessage)                    
            else:
                self.speak('There is nothing there.')
                
    @intent_file_handler('inventory remove.intent')
    def handle_inventoryremove(self, message):
        self.obj = message.data.get('obj');
        with open(inventoryfile, 'r') as inp, open(editfile, 'w') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if row[0] != self.obj:
                    writer.writerow(row)
        self.speak('Removed')
        shutil.copyfile(editfile,inventoryfile)
        
    @intent_file_handler('inventory add.intent')
    def handle_inventoryadd(self, message):
        self.obj = message.data.get('obj');
        self.loc = message.data.get('loc');
        addlist=[(self.obj,self.loc)]
        with open(inventoryfile, 'r') as inp, open(editfile, 'w') as out:
            writer = csv.writer(out)
            writer.writerows(addlist)
            for row in csv.reader(inp):
                writer.writerow(row)
        self.speak("Added")      
        shutil.copyfile(editfile,inventoryfile)

    @intent_file_handler('inventory move.intent')
    def handle_inventorymove(self, message):
        self.obj = message.data.get('obj');
        self.loc = message.data.get('loc');
        addlist=[(self.obj,self.loc)]
        with open(inventoryfile, 'r') as inp, open(editfile, 'w') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if row[0] == self.obj:
                    writer.writerows(addlist)
                    self.speak('Moved')
                else:
                    writer.writerow(row)
        shutil.copyfile(editfile,inventoryfile)

def create_skill():
    return Inventory()
