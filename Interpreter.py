from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Interpreter:

    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

        task_sentence = ["Can I have?", "May I have?", "I want", "Let me have", "I would like", "Get me",
                         "How much is?",
                         "What's the damage?"]

        confirmation_commands = ["yes", "yeah", "ya", "yep", "yup", "that's correct", "correct", "no", "nope", "nah"]
        self.menu_items = ["burger", "fries", "coke", "nuggets"]

        self.confirmation_embeddings = self.model.encode(confirmation_commands)
        self.task_embeddings = self.model.encode(task_sentence)
        self.item_embeddings = self.model.encode(self.menu_items)

    def interpret(self, user_input):
        embedded_input = self.model.encode([user_input])

        action = self.get_action(embedded_input)

        if action == 1:
            response = "You want "
        else:
            response = "You asked for the price of "

        item = self.get_item(embedded_input)

        return action, item, response + item + ", is that right?"

    def get_action(self, embedded_input):
        similarities = []
        for i in range(len(self.task_embeddings)):
            if i < 6:
                similarities.append([cosine_similarity([self.task_embeddings[i]], embedded_input)[0], 1])
            else:
                similarities.append([cosine_similarity([self.task_embeddings[i]], embedded_input)[0], 2])

        similarities.sort(key=lambda similarities: similarities[0], reverse=True)

        return similarities[0][1]

    def get_item(self, embedded_input):
        similarities = []
        for i in range(len(self.item_embeddings)):
            similarities.append([cosine_similarity([self.item_embeddings[i]], embedded_input)[0], i])

        similarities.sort(key=lambda similarities: similarities[0], reverse=True)
        return self.menu_items[similarities[0][1]]

    def confirm(self, user_input):
        embedded_input = self.model.encode([user_input])
        similarities = []
        for i in range(len(self.confirmation_embeddings)):
            if i < 7:
                similarities.append([cosine_similarity([self.confirmation_embeddings[i]], embedded_input)[0], 1])
            else:
                similarities.append([cosine_similarity([self.confirmation_embeddings[i]], embedded_input)[0], 0])

        similarities.sort(key=lambda similarities: similarities[0], reverse=True)

        return similarities[0][1]
