import datetime

class Rappel:
    def __init__(self, description, heure):
        self.description = description
        self.heure = heure

    def est_l_heure(self):
        maintenant = datetime.datetime.now().time()
        return maintenant >= self.heure

    def afficher_rappel(self):
        return f"Rappel : {self.description} à {self.heure}"