import numpy as np 
import matplotlib.pyplot as plt 
import random 

from copy import deepcopy 



class Eleve():  
    def __init__(self,id):

        formations = [1,2,3,4,5] #Liste des 5 formations existantes
        formations_copy = deepcopy(formations) #Copy pour ne pas avoir de problème d'addresse et de même instance
        random.shuffle(formations_copy) #Le Choix des étudiants est une liste de préférence des 5 formations triés par ordre décroissant 
       
        
        self.voeux = formations_copy #Voeux de l'étudiant qui n'est simplement que la liste des formations dans le désordre

        self.id = id #Identifiant de l'étudiant

        self.a_trouve_un_voeu = False #L'étudiant n'a pas encore de voeu

        self.noteMaths = random.randrange(20) #L'étudiant a des notes de 0-20 attribué au hasard
        self.noteFrançais = random.randrange(20)
        self.notePhysiqueChimie = random.randrange(20)
        self.notePhylosophie = random.randrange(20)
        self.noteSvt = random.randrange(20)

        self.listeNotes = [ self.noteMaths,self.noteFrançais,self.notePhysiqueChimie,self.notePhylosophie,self.noteSvt ] #La liste de toutes les notes de l'élèves

    def getEleveId(self):
        return self.id

    def getBulletin(self):
        return self.listeNotes
    
    def getChoix(self): #Les étudiants n'ont le droit qu'à trois voeux
        return self.voeux[0:3] 
    
    def getPositionementFormation(self,voeu): #Donne le positionement de la formation dans la liste des voeux de l'élève
        return self.voeux[0:3].index(voeu)

    def aTrouveUnVoeu(self):
        self.a_trouve_un_voeu = True
    
    def getEleveEtat(self):
        return self.a_trouve_un_voeu
    
    def getSatisfactionEleve(self,id_formation): #renvoie le niveau de satisfaction de l'élève par rapport au choix de sa formation
        if(self.getPositionementFormation(id_formation)==0): #Premier choix de l'élève, donc le plus satisfaisant
            return 3
        if(self.getPositionementFormation(id_formation)==1): #Deuxième choix de l'élève, donc une satisfaction moyenne
            return 2
        else: #Troisième choix, le moins satisfaisant
            return 1





class Formation():
    def __init__(self,id,listeEleves, listeCoeff):
        self.listeCoeff = listeCoeff
        self.id = id
        
        dict_eleve_note= {}
        
        for eleve in listeEleves:
            note_eleve = 0 #Cette note permettra de faire un classement des élèves pour les formations
            bulletin = eleve.getBulletin()
            note_eleve += (bulletin[0] * listeCoeff[0] + bulletin[1] * listeCoeff[1] + bulletin[2] * listeCoeff[2] + bulletin[3] * listeCoeff[3] + bulletin[4] * listeCoeff[4])/15 
            dict_eleve_note[eleve] = note_eleve

       
        dict_eleve_note_triee = sorted(dict_eleve_note,key=dict_eleve_note.get, reverse=True)

        self.listeEleves = dict_eleve_note_triee
        self.listeElevesAcceptés = []

    def getEleveTriee(self):
        return self.listeEleves
    
    def ajoutEleveAccepté(self,eleve):
        self.listeElevesAcceptés.append(eleve)
    
    def getPositionementEleve(self,eleve):
        return self.listeEleves.index(eleve)
    
    def getNombreEleveAccepté(self):
        return len(self.listeElevesAcceptés)

    def EleveDejaAccepté(self,eleve):
        return eleve in self.listeElevesAcceptés
    
    def remove(self,eleve):
        self.listeElevesAcceptés.remove(eleve)
    
    def append(self,eleve):
        self.listeElevesAcceptés.append(eleve)
    
    def getElevesAcceptés(self):
        return self.listeElevesAcceptés

    def getIdFormation(self):
        return self.id
    
    


class APB():
    def __init__(self,listeEleves,listeFormations):
        self.listeEleves = listeEleves
        self.listeFormations = listeFormations
    
    def affectation_phase_un(self): #toutes les formations obtiennent leur meilleur choix
        for eleve in self.listeEleves: #on regarde parmi les choix des élèves dans quels formations ils sont le mieux classé, et dès lorsque celle-ci n'ont toujours pas atteint le nombre max d'élèves on les ajoute
            if (min(self.listeFormations[eleve.getChoix()[0]-1].getPositionementEleve(eleve),
            self.listeFormations[eleve.getChoix()[1]-1].getPositionementEleve(eleve),
            self.listeFormations[eleve.getChoix()[2]-1].getPositionementEleve(eleve)) == self.listeFormations[eleve.getChoix()[0]-1].getPositionementEleve(eleve)):
                if (self.listeFormations[eleve.getChoix()[0]-1].getNombreEleveAccepté() < 50):
                    self.listeFormations[eleve.getChoix()[0]-1].ajoutEleveAccepté(eleve)
    
                    

            if (min(self.listeFormations[eleve.getChoix()[0]-1].getPositionementEleve(eleve),
            self.listeFormations[eleve.getChoix()[1]-1].getPositionementEleve(eleve),
            self.listeFormations[eleve.getChoix()[2]-1].getPositionementEleve(eleve)) == self.listeFormations[eleve.getChoix()[1]-1].getPositionementEleve(eleve)):
                if (self.listeFormations[eleve.getChoix()[1]-1].getNombreEleveAccepté() < 50):
                    self.listeFormations[eleve.getChoix()[1]-1].ajoutEleveAccepté(eleve)  
                      

            if (min(self.listeFormations[eleve.getChoix()[0]-1].getPositionementEleve(eleve),
            self.listeFormations[eleve.getChoix()[1]-1].getPositionementEleve(eleve),
            self.listeFormations[eleve.getChoix()[2]-1].getPositionementEleve(eleve)) == self.listeFormations[eleve.getChoix()[2]-1].getPositionementEleve(eleve)):
                if (self.listeFormations[eleve.getChoix()[2]-1].getNombreEleveAccepté() < 50):
                    self.listeFormations[eleve.getChoix()[2]-1].ajoutEleveAccepté(eleve)
                    
                    
       
    
    def affectation_phase_deux(self): #stabilisation des couples. Recherche d'une formation mieux classé dans les choix des élèves 
        for eleve in self.listeEleves:
            if (self.listeFormations[eleve.getChoix()[0]-1].getPositionementEleve(eleve) == self.listeFormations[eleve.getChoix()[1]-1].getPositionementEleve(eleve)):
                if(self.listeFormations[eleve.getChoix()[0]-1].EleveDejaAccepté(eleve)):
                    print("")
                if(self.listeFormations[eleve.getChoix()[1]-1].EleveDejaAccepté(eleve)):
                    self.listeFormations[eleve.getChoix()[1]-1].remove(eleve) 
                    if(self.listeFormations[eleve.getChoix()[0]-1].getNombreEleveAccepté() < 50):
                        self.listeFormations[eleve.getChoix()[0]-1].append(eleve)
                
                    
            if (self.listeFormations[eleve.getChoix()[0]-1].getPositionementEleve(eleve) == self.listeFormations[eleve.getChoix()[2]-1].getPositionementEleve(eleve)):
                if(self.listeFormations[eleve.getChoix()[0]-1].EleveDejaAccepté(eleve)):
                    print("")
                if(self.listeFormations[eleve.getChoix()[2]-1].EleveDejaAccepté(eleve)):
                    self.listeFormations[eleve.getChoix()[2]-1].remove(eleve) 
                    if(self.listeFormations[eleve.getChoix()[0]-1].getNombreEleveAccepté() < 50):
                        self.listeFormations[eleve.getChoix()[0]-1].append(eleve)
                
            if (self.listeFormations[eleve.getChoix()[1]-1].getPositionementEleve(eleve) == self.listeFormations[eleve.getChoix()[2]-1].getPositionementEleve(eleve)):
                if(self.listeFormations[eleve.getChoix()[1]-1].EleveDejaAccepté(eleve)):
                    print("")
                if(self.listeFormations[eleve.getChoix()[2]-1].EleveDejaAccepté(eleve)):
                    self.listeFormations[eleve.getChoix()[2]-1].remove(eleve) 
                    if(self.listeFormations[eleve.getChoix()[1]-1].getNombreEleveAccepté() < 50):
                        self.listeFormations[eleve.getChoix()[1]-1].append(eleve)
                
        
        
    

class Parcoursup():
    def __init__(self,listeEleves,listeFormations):
        self.listeEleves = listeEleves
        self.listeFormations = listeFormations
        self.listeElevesSansFormations = []

    def affectation_phase_un(self):
        for eleve in self.listeEleves:
            choix = random.choice(eleve.getChoix())
            
            for formation in self.listeFormations:
                if (formation.getIdFormation() == choix):
                    if(formation.getNombreEleveAccepté() < 50):
                        formation.append(eleve)
                    else:
                        self.listeElevesSansFormations.append(eleve)
                    
                    
        
    
    def affectation_phase_deux(self):


        for eleve in self.listeElevesSansFormations:

            listeChoixEleve = []
            
            for formation in self.listeFormations:
                if (formation.getIdFormation() in eleve.getChoix()):
                    listeChoixEleve.append(formation)


            for formation in listeChoixEleve:
                if (formation.getNombreEleveAccepté() < 50):
                    if (eleve.a_trouve_un_voeu == False):
                        formation.append(eleve)
                        eleve.a_trouve_un_voeu = True
        
                

                    
all_satisfaction_APB = [] 
all_satisfaction_Parcoursup = []  
all_nonAdmis_APB = []
all_nonAdmis_Parcoursup = []     
for i in range(200): #nombre de répétitions de simulations
    listeEleves = [] #création d'une liste d'élèves
    listeFormations = [] #création d'une liste de formations
    for i in range(250): #remplissage de la liste de 250 élèves
        eleve = Eleve(i)
        listeEleves.append(eleve)

    listeCoeff1 = [5,2,3,1,4] #Coefficient qui permettra de donner le niveau d'appréciation d'un formation vis-à-vis d'un candidat
    formation1 = Formation(1,listeEleves,listeCoeff1) 
    listeCoeff2 = [1,4,2,5,3]
    formation2 = Formation(2,listeEleves,listeCoeff2)
    listeCoeff3 = [4,3,1,2,5]
    formation3 = Formation(3,listeEleves,listeCoeff3)
    listeCoeff4 = [3,1,5,4,2]
    formation4 = Formation(4,listeEleves,listeCoeff4)
    listeCoeff5 = [2,5,4,3,1]
    formation5 = Formation(5,listeEleves,listeCoeff5)


    listeFormations = [formation1,formation2,formation3,formation4,formation5]
    listeEleves_copy = deepcopy(listeEleves)
    listeFormations_copy = deepcopy(listeFormations)

    apb = APB(listeEleves, listeFormations)

    apb.affectation_phase_un()
    apb.affectation_phase_deux()

    Satisfaction_étudiante_APB = 0
    Eleve_sans_formation_APB = 0

    for formation in listeFormations:
        for eleve in formation.getElevesAcceptés():
            Satisfaction_étudiante_APB += eleve.getSatisfactionEleve(formation.getIdFormation())
        Eleve_sans_formation_APB += (50 - formation.getNombreEleveAccepté())   

    # print("Satisfaction étudiante : ")
    # print(((Satisfaction_étudiante_APB / 750) * 100))
    # print("Eleves sans formation: ")
    # print(Eleve_sans_formation_APB)
    # print((Eleve_sans_formation_APB/250)*100)

    parcoursup = Parcoursup(listeEleves_copy, listeFormations_copy)

    parcoursup.affectation_phase_un()
    parcoursup.affectation_phase_deux()

    Satisfaction_étudiante_PARCOURSUP = 0
    Eleve_sans_formation_PARCOURSUP = 0

    for formation in listeFormations_copy:
        for eleve in formation.getElevesAcceptés():
            Satisfaction_étudiante_PARCOURSUP += eleve.getSatisfactionEleve(formation.getIdFormation())
        Eleve_sans_formation_PARCOURSUP += (50 - formation.getNombreEleveAccepté())  

    # print("Satisfaction étudiante : ")
    # print(((Satisfaction_étudiante_PARCOURSUP / 750) * 100))
    # print("Eleves sans formation: ")
    # print(Eleve_sans_formation_PARCOURSUP)
    # print((Eleve_sans_formation_PARCOURSUP/250)*100)

    all_satisfaction_APB.append((Satisfaction_étudiante_APB/750) * 100)
    all_satisfaction_Parcoursup.append((Satisfaction_étudiante_PARCOURSUP/750)*100)
    all_nonAdmis_APB.append((Eleve_sans_formation_APB/250)*100)
    all_nonAdmis_Parcoursup.append((Eleve_sans_formation_PARCOURSUP/250)*100)

np_aw_t = np.transpose(np.array(all_satisfaction_APB))
np_aw_t1 = np.transpose(np.array(all_satisfaction_Parcoursup))

bins = np.linspace(55, 75, 50)

plt.title("Satisfaction des élèves (sur 200 simulations)")
plt.xlabel("Pourcentage de satisfaction chez les 250 élèves", fontsize=10)  
plt.ylabel("Nombre de simulations", fontsize=10)
plt.hist(np_aw_t, bins, alpha=0.5, label='APB')
plt.hist(np_aw_t1, bins, alpha=0.5, label='Parcoursup')
plt.legend(loc='upper right')
plt.show()

np_aw_t = np.transpose(np.array(all_nonAdmis_APB))
np_aw_t1 = np.transpose(np.array(all_nonAdmis_Parcoursup))

bins = np.linspace(0, 10, 10)

plt.title("Nombre de Non_Admis(sur 200 simulations)")
plt.xlabel("Nombre de Non_Admis (Dans un ensembre de 250 candidats)", fontsize=10)  
plt.ylabel("Nombre de simulations", fontsize=10)
plt.hist(np_aw_t, bins, alpha=0.5, label='APB')
plt.hist(np_aw_t1, bins, alpha=0.5, label='Parcoursup')
plt.legend(loc='upper right')
plt.show()

