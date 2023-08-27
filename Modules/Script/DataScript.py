from Modules.Person import DataPerson
from Modules.Place import DataPlace
from Modules.Script import setScript
from Modules.Tools import Singleton
from Modules.Tools.Style import color

class DataScript (metaclass=Singleton.Singleton):
    __nextIdScript = 1

    def __init__(self):
        self.__script=dict()

    def __incrementScript(self):
        self.__nextIdScript += 1

    def __getIdScript(self):
        return self.__nextIdScript

    def getScripts(self) :
        l = list()
        for key in self.__script.keys():
            l.append(key)
        return l

    def getScript(self, script) :
        if script not in self.getScripts():
            print(f"\n{color.RED}Error : {color.BLUE}{script}{color.RESET} not in scripts")
            return None
        else :
            return self.__script[script]

    def addScript(self, person, day, type=None, **kwargs) :
        dataperson = DataPerson.DataPerson()
        id = self.__getIdScript()
        while id in self.getScripts():
            self.__incrementScript()
            id = self.__getIdScript()
        if person in dataperson.getPeople() :
            self.__script[id] = self.Script (id, person, day, type=type, **kwargs)
            print(f"Script {color.BLUE}{id}{color.RESET} has been added to scripts")
            dataperson.getPerson(person).addScript(id, change=True)
            return id
        else :
            print(f"{color.RED}Error : {color.CYAN}{type}{color.RESET} not in types")
            return None

    def removeScript(self, id) :
        dataperson = DataPerson.DataPerson()
        if id in DataScript().getScripts() :
            del self.__script[id]
            print(f"Script {color.BLUE}{id}{color.RESET} has been deleted from scripts")
        else :
            print(f"{color.RED}Error : {color.BLUE}{id}{color.RESET} not in scripts" )

    def __str__(self) :
        kwargs = dict()
        kwargs["indent"]=1
        string = f"{color.UNDERLINE}DataScript :{color.RESET}"
        for script in self.getScripts() :
            string += f"\n\n{self.getScript(script).__str__(**kwargs)}"
        return string

    def __repr__(self):
        return self.__str__()

    class Script ():
        def __init__(self, id, person, day, type=None, **kwargs):
            self.__id = id
            self.__person = person
            self.__day = day
            if setScript.checkTypeScript(type) :
                self.__sequence = setScript.applyTypeScript(type, person, day, **kwargs)
            else :
                self.__sequence = setSequence(type=None, select=True, change=False)

        def getId(self) :
            return self.__id

        def getPerson(self) :
            return self.__person

        def getDay(self) :
            return self.__day

        def getSequence(self) :
            return self.__sequence

        def setSequence(self, type=None, select=False, change=False, **kwargs) :
            if not setScript.checkTypeScript(type) :
                if select == None :
                    print(f"{color.RED}Error : {color.RESET}No sequence referenced" )
                else :
                    type = setScript.selectTypeScript()
            if setScript.checkTypeScript(type) :
                if self.getSequence() != None :
                    if change==True :
                        self.__sequence = setScript.applyTypeScript(type, self.getPerson(), self.getDay(), **kwargs)
                    else :
                        print(f"{color.RED}Error : {color.RESET}A sequence has already been set" )
                else :
                    self.__sequence = setScript.applyTypeScript(type, self.getPerson(), self.getDay(), **kwargs)

        def __str__(self, **kwargs) :
            indent = kwargs.get("indent", 0)
            string = "\t"*indent + f"{color.UNDERLINE}Script :{color.RESET} {color.BLUE}{self.getId()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"person : {color.CYAN}{self.getPerson()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"day : {color.CYAN}{self.getDay()}{color.RESET}"
            sequence = self.getSequence()
            if sequence != None :
                string += "\n\t" + "\t"*indent + "Sequence :"
                for elem in sequence :
                    string += "\n\t\t" + "\t"*indent + f"{elem}"
            return string

        def __repr__(self):
            return self.__str__()
