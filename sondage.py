class Sondage:
    def __init__(self, question, options):
        self.question = question
        self.options = options
        self.votes = {option: 0 for option in options}

    def ajouter_vote(self, option):
        if option in self.options:
            self.votes[option] += 1

    def afficher_resultats(self):
        resultats = "Résultats du sondage :\n"
        for option, votes in self.votes.items():
            resultats += f"{option}: {votes} vote(s)\n"
        return resultats
    