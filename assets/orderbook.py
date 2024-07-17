import pandas as pd
import datetime as dt
import random

class Ordre:

    def __init__(self, tick, lot):
        colonnes=['ref','trader','horodatage','type','prix','montant','maker']
        self.carnetachat=pd.DataFrame(columns=colonnes)
        self.carnetvente=pd.DataFrame(columns=colonnes)
        self.tick=tick
        self.lot=lot
    
    def ordre_check(self,prix,montant):
        if (prix% self.tick)>0.01 or (montant%self.lot)>0.01:
            print('Contraintes de tick et/ou de lot non respectées.')
            return False
        return True

    def ordre(self,trader,horodatage,type,prix,montant,maker):
        if self.ordre_check == False:
            return
        ref=str(horodatage) + str(round(random.random()*100000))
        nouvelordre={'ref':ref,
                'trader':trader,
                'horodatage':horodatage,
                'type':type,
                'prix':prix,
                'montant':montant,
                'maker':maker}
        if maker=="maker":
            if type == 'achat':
                if not(self.carnetvente.empty):
                    while prix>=self.carnetvente.loc[0,'prix'] and montant>0:
                        if montant>=self.carnetvente.loc[0,'montant']:
                            montant-=self.carnetvente.loc[0,'montant']
                            self.carnetvente.drop(index=0, inplace=True)
                            self.carnetvente.reset_index(drop=True,inplace=True)
                        else:
                            self.carnetvente.loc[0,'montant']-=montant
                            montant=0
                            return    
                self.carnetachat = pd.concat([self.carnetachat, pd.DataFrame([nouvelordre])], ignore_index=True)
                self.carnetachat.sort_values(by=['prix','montant','horodatage'], ascending=[False,False,True], inplace=True)
            elif type == 'vente':
                if not(self.carnetachat.empty):
                    while prix<=self.carnetachat.loc[0,'prix'] and montant>0:
                        if montant>=self.carnetachat.loc[0,'montant']:
                            montant-=self.carnetachat.loc[0,'montant']
                            self.carnetachat.drop(index=0, inplace=True)
                            self.carnetachat.reset_index(drop=True,inplace=True)
                        else:
                            self.carnetachat.loc[0,"montant"]-=montant
                            montant=0
                            return
                self.carnetvente=pd.concat([self.carnetvente, pd.DataFrame([nouvelordre])],ignore_index=True)
                self.carnetvente.sort_values(by=['prix','montant','horodatage'],ascending=[True,False,True],inplace=True)
                self.carnetvente.reset_index(drop=True,inplace=True)
            else:
                print("Erreur de type d'ordre. Spécifier achat ou vente")
                return
        elif maker=='taker':
            self.taker_exec(nouvelordre)
        
    def taker_exec(self, taker_order):
        if type=='achat':
            self.carnetvente.sort_values(by=['prix','montant','horodatage'], ascending=[True,False,True], inplace=True)
            self.carnetvente.reset_index(drop=True,inplace=True)
            carnet_type=self.carnetvente
        elif type=='vente':
            self.carnetachat.sort_values(by=['prix','montant','horodatage'],ascending=[False,False,True],inplace=True)
            self.carnetachat.reset_index(drop=True,inplace=True)
            carnet_type=self.carnetachat

        outstanding=taker_order['montant']
        while outstanding !=0:
            for i, ordre in carnet_type.iterrows():
                if outstanding>=ordre:
                    self.carnet_type.drop(index=0,inplace=True)
                    self.carnet_type.reset_index(drop=True,inplace=True)
                    outstanding-=ordre
                else:
                    ordre['montant']-=outstanding
                    outstanding=0
            break

        if outstanding>0:
            horodatage=dt.now().isoformat()
            maker='maker'
            ordre = {'trader':ordre['trader'],
                'horodatage':horodatage,
                'type':ordre['type'],
                'prix': ordre['prix'], 
                'montant': outstanding,
                'maker':maker
                }
            if ordre['type']=='vente':
                self.carnetvente = self.carnetvente._append(ordre, ignore_index=True)
                self.carnetvente.sort_values(by=['prix', 'montant','horodatage'], ascending=[True, False,True], inplace=True)
                self.carnetvente.reset_index(drop=True,inplace=True)
            else:
                self.carnetachat = self.carnetachat._append(ordre, ignore_index=True)
                self.carnetachat.sort_values(by=['prix', 'montant','horodatage'], ascending=[False,False, True], inplace=True)
                self.carnetachat.reset_index(drop=True,inplace=True)
            
    def order_delete(self,type,trader,montant,prix):
        if type=='achat':
            row_index=self.carnetachat[(self.carnetachat['trader']==trader) & (self.carnetachat['montant']==montant) & (self.carnetachat['prix']==prix)].index[0]
            self.carnetachat=self.carnetachat.drop(row_index)
            self.carnetachat.reset_index(drop=True,inplace=True)
        if type=='vente':
            row_index=self.carnetvente[(self.carnetachat['trader']==trader) & (self.carnetvente['montant']==montant) & (self.carnetvente['prix']==prix)].index[0]
            self.carnetvente=self.carnetvente.drop(row_index)
            self.carnetvente.reset_index(drop=True,inplace=True)

exemple = Ordre(tick=0.01, lot=1)

import random
from datetime import datetime, timedelta




random_dates = []
for _ in range(3000):
    random_days = random.randint(1, 365)
    random_hours = random.randint(0, 23)
    random_date = datetime.now() - timedelta(days=random_days, hours=random_hours)
    random_dates.append(random_date)

noms=['Aurélie','Diane','Thibaut','Adele','Loïc','Mathieu','Karim','Victor','Samia','Lenaïg']

exemple.ordre('Josep',random_dates[1],'achat',177.8,30,'maker')
exemple.ordre('Maria',random_dates[2],'achat',179.2,10,'maker')
exemple.order_delete('achat','Josep',30,177.8)
for i in range (1000):
    exemple.ordre(noms[round(random.random()*10)-1],random_dates[2*i+2],'vente',178+(round(random.random(),2)-0.5)*10,round(random.random()*100+random.random()*10,2),'maker')
    exemple.ordre(noms[round(random.random()*10-1)],random_dates[i+2],'achat',178+(round(random.random(),2)-0.5)*10,round(random.random()*100+random.random()*10,2),'maker')

print(exemple.carnetachat)
print(exemple.carnetvente)