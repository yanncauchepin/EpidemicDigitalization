'''----------------------------------------------------------------> DEPRECATED



from Modules.Person import DataPerson
from Modules.Data import Luxembourg
from Modules.Tools.Style import color
import random

def getTypeAgeDivisionLuxembourg (type) :

    dataperson = DataPerson.DataPerson()
    demographic = Luxembourg.Demographic()

    if type not in dataperson.getTypes():
        print(f"{color.RED}Error : {color.CYAN}{type}{color.RESET} not in types")
        return None
    else :
        type = dataperson.getType(type)
        division = list()
        age_distrib = demographic.getDistribAge()
        size = len(age_distrib)
        for subtype in type.getSubtypes():
            age_min = type.getSubtype(subtype).getFeature("age_min")
            if age_min !=None :
                if int(age_min) < 0 or int(age_min) > size-2 :
                    age_min=0
            else :
                age_min = 0
            age_max = type.getSubtype(subtype).getFeature("age_max")
            if age_max !=None :
                if int(age_max)>size-1 or int(age_max)<1 :
                    age_max = size-1
            else :
                age_max = size-1
            if int(age_max)<int(age_min) :
                age_min = 0
                age_max = size-1
            for i in range(age_min, age_max+1):
                    division.append(age_distrib[i]+[type.getSubtype(subtype).getName()])
        sum = 0
        delete = list()
        for i in range(len(division)):
            if len(division[i])<3:
                delete.append(i)
            else :
                sum += division[i][1]
        delete.sort(reverse=True)
        for i in delete:
            del division[i]
        cumul = 0
        for i in range (len(division)):
            cumul+=division[i][1]*100/sum
            division[i][1]=round(cumul,4)

        return division

def setTypePeople(type, number):

    dataperson = DataPerson.DataPerson()
    if type not in dataperson.getTypes():
        print(f"{color.RED}Error : {color.CYAN}{type}{color.RESET} not in types")
        return None
    else :
        division = getTypeAgeDivisionLuxembourg(type=type)
        if number > 0 :
            for i in range(number):
                r = random.random()*100
                age = 0
                while (age < len(division) and r > division[age][1]) :
                    age+=1
                if len(division[age]) > 3 :
                    subtype = random.choice(division[age][2:])
                    dataperson.addPerson(age=division[age][0], type=type, subtype=subtype, autoId=True)
                else :
                    dataperson.addPerson(age=division[age][0], type=type, subtype=division[age][2], autoId=True)
        else :
            print(f"{color.RED}Error : {color.CYAN}number {number}{color.RESET} must be an int greater than 0")
'''