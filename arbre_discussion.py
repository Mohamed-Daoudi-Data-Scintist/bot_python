class TreeNode:
    def __init__(self, question, yes_node=None, no_node=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node


class ConversationBot:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.topic_list = set()

    def add_topic(self, topic):
        self.topic_list.add(topic)

    def create_tree(self):
        # Niveau 1
        root_question = "Tape 1 pour la programmation,tape 2 pour la cuisine"

        # Niveau 2
        question1 = "Tape 1 pour un language specifique,tape 2 pour du debogage"
        question2 = "Tape 1 pour des recettes de cuisine spécifiques,tape 2 des conseils sur les techniques de cuisson ?"

        # Niveau 3 - Programmation
        question3 = "Tape 1 pour apprendre le Python, tape 2 pour apprendre le Java"
        question4 = "Tape 1 si vous rencontrez des erreurs de syntaxe, tape 2 vous rencontrez des erreurs d'exécution ?"

        # Niveau 3 - Cuisine
        question5 = "Tape 1 pour des recettes de cuisine asiatique, tape 2 pour des recettes de cuisine italienne ?"
        question6 = "Tape 1 pour des conseils sur la cuisson au four, tape 2 pour des conseils sur la cuisson à la poêle ?"

        # Niveau 4 - Langages de programmation
        question7 = "Fin de la conversation j'ai plus d'inspi"
        question8 = "Fin de la conversation j'ai plus d'inspi"

        # Niveau 4 - Débogage
        question9 = "Fin de la conversation j'ai plus d'inspi?"
        question10 = "Fin de la conversation j'ai plus d'inspi"

        # Niveau 4 - Recettes de cuisine
        question11 = "Fin de la conversation j'ai plus d'inspi"
        question12 = "Fin de la conversation j'ai plus d'inspi"

        # Niveau 4 - Techniques de cuisson
        question13 = "Fin de la conversation j'ai plus d'inspi"
        question14 = "Fin de la conversation j'ai plus d'inspi"

        # Création de l'arbre binaire
        node7 = TreeNode(question7)
        node8 = TreeNode(question8)

        node9 = TreeNode(question9)
        node10 = TreeNode(question10)

        node11 = TreeNode(question11)
        node12 = TreeNode(question12)

        node13 = TreeNode(question13)
        node14 = TreeNode(question14)

        node3 = TreeNode(question3, node7, node8)
        node4 = TreeNode(question4, node9, node10)

        node5 = TreeNode(question5, node11, node12)
        node6 = TreeNode(question6, node13, node14)

        node1 = TreeNode(question1, node3, node4)
        node2 = TreeNode(question2, node5, node6)

        self.root = TreeNode(root_question, node1, node2)
        self.current_node = self.root

    def reset_conversation(self):
        self.current_node = self.root

    def response(self, user_input):
        if user_input.lower() == "reset":
            self.reset_conversation()
            return "La conversation a été réinitialisée. Comment puis-je vous aider ?"

        if user_input.lower().startswith("speak about"):
            topic = user_input[11:]
            if topic.lower() in self.topic_list:
                return f"Oui, je peux vous parler de {topic}. Quelle est votre question à ce sujet ?"
            else:
                return f"Désolé, je ne peux pas vous parler de {topic}."

        if user_input.lower() == "help":
            return self.start_conversation()


        if self.current_node is None:
            return "La conversation a atteint une impasse. Veuillez réinitialiser la conversation."
        
        if self.current_node.yes_node is None and self.current_node.no_node is None:
            return f"Votre besoin est : {self.current_node.question}. Comment puis-je vous aider ?"

        if user_input.lower() == "1" and self.current_node.yes_node:
            self.current_node = self.current_node.yes_node
        elif user_input.lower() == "2" and self.current_node.no_node:
            self.current_node = self.current_node.no_node
        else:
            return "Je ne comprends pas votre réponse. Veuillez répondre par '1' ou '2'."

        return self.current_node.question



    def start_conversation(self):
        self.current_node = self.root
        return self.current_node.question
    
    def main():
        bot = ConversationBot()
        bot.add_topic("programmation")
        bot.add_topic("cuisine")
        bot.create_tree()

        print("Bienvenue dans la conversation avec le bot. Tapez 'help' pour commencer.")
        while True:
            user_input = input("Vous: ")
            bot_response = bot.response(user_input)
            print("Bot:", bot_response)

    if __name__ == "__main__":
        main()
