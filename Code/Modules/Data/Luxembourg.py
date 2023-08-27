from Modules.Tools import Singleton
import csv

class Demographic(metaclass=Singleton.Singleton):
    #https://statistiques.public.lu/fr/index.html
    def __init__(self):
        self._age_distrib = self._initDistribAge()
        self._population_region = self._initPopulationRegion("Canton Luxembourg")

    def _initDistribAge(self) :
        age_distrib = list()
        fichier="Modules/Data/age_distribution.csv"
        with open(fichier, newline="") as csvfile :
            reader = csv.reader(csvfile, delimiter=",")
            lreader = list(zip(*reader))
            distrib = list(lreader[4][5:])
            age = list(lreader[0][5:])
        j = 0
        for i in range(len(age)):
            if i%6==0:
                j+=1
            else :
                age_distrib.append([int(i-j),float(distrib[i])])
        return age_distrib

    def getDistribAge(self,age_min=0, age_max=95, cumul=None) :
        if int(age_min) < 0 or int(age_min) >len(self._age_distrib)-2 :
            age_min=0
        if int(age_max)>len(self._age_distrib)-1 or int(age_max)<1 :
            age_max = len(self._age_distrib)-1
        if int(age_max)<int(age_min) :
            return None
        somme = 0
        for i in range(age_min, age_max+1) :
            somme += self._age_distrib[i][1]
        age_distrib=list()
        if cumul ==None :
            for i in range(age_min, age_max+1) :
                age_distrib.append([int(i), round(self._age_distrib[i][1]*100/somme,4)])
        else :
            cumul = 0
            for i in range(age_min, age_max+1) :
                cumul += self._age_distrib[i][1]*100/somme
                age_distrib.append([int(i), round(cumul,4)])
        return age_distrib

    def _initPopulationRegion(self, region) :
        fichier="Modules/Data/population_per_region.csv"
        with open(fichier, newline="") as csvfile :
            reader = csv.reader(csvfile, delimiter=",")
            lreader=list(zip(*reader))
            if str(region) not in lreader[0] :
                number = 0
            else :
                number = int(lreader[-1][lreader[0].index(str(region))])
        return number

    def getPopulationRegion(self, region=None):
        if region==None :
            return self._population_region
        else :
            return self._initPopulationRegion(region)
