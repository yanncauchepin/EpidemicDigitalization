from Modules.Person import DataPerson
from Modules.Script import DataScript, setScript
from Modules.Tools.Style import color

def initPeopleScript(people, day, type=None, **kwargs):

    datascript = DataScript.DataScript()
    dataperson = DataPerson.DataPerson()

    if not setScript.checkTypeScript(type) :
        print(f"{color.RED}Error : {color.RESET}No sequence referenced" )
        type = DataScript.selectTypeScript()
    if setScript.checkTypeScript(type) :
        for person in people :
            if person in dataperson.getPeople() :
                datascript.addScript(person, day, type, **kwargs)
            else :
                print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{person}{color.RESET}not in dataperson")
