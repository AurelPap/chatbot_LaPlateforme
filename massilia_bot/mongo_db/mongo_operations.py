from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
from constants import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME, PATH, FILENAME
import random
import logging


class MongoOperations:
    def __init__(self, uri=MONGODB_URI, db_name=DATABASE_NAME, collection_name=COLLECTION_NAME):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def __enter__(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        print("MongoDB connection closed.")

    def delete_data(self):
        self.collection.drop()
        print("Collection 'chatbot' supprimée.")
        print(f"Nombre de documents dans la collection après la suppression : {self.collection.count_documents({})}")



    def add_data(self, q_and_a_list):
        count_documents_before = self.collection.count_documents({})
        print(f"Nombre de documents dans la collection avant l'insertion : {count_documents_before}")

        if not all(isinstance(item, dict) for item in q_and_a_list):
            raise ValueError("Le(s) dictionnaires d'entrés doivent contenir 'tag', 'patterns' et 'responses'")
        documents = self.fetch_data()

        # transforme le json en dict
        existing_data = {doc['tag']: doc for doc in documents}

        for new_entry in q_and_a_list:
            tag = new_entry['tag']
            if tag in existing_data:
                existing_data[tag]['patterns'].extend(new_entry['patterns'])
                existing_data[tag]['responses'].extend(new_entry['responses'])
            else:
                existing_data[tag] = new_entry

        self.delete_data()
        self.collection.insert_many(list(existing_data.values()))

        count_documents_after = self.collection.count_documents({})
        print(f"Nombre de documents dans la collection après l'insertion : {count_documents_after}")

    def fetch_data(self):
            documents = list(self.collection.find())
            print("Les données ont bien été récupérés")
            return documents

    def reset_data(self):
        self.collection.drop()

        file_path = f"{PATH}/{FILENAME}" if PATH else FILENAME
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if data['intents'] exists and is a list
        if 'intents' in data and isinstance(data['intents'], list) and data['intents']:
            print(f"Opened json file with {len(data['intents'])} intents.")
            self.collection.insert_many(data['intents'])
            print("La db a été réinitialisée avec les données du fichier")
        else:
            raise ValueError("The JSON file does not contain a non-empty 'intents' list")



with MongoOperations() as mongo_ops:
    print('-----------------delete')
    mongo_ops.delete_data()
    print('-----------------reset')
    mongo_ops.reset_data()

    print('-----------------add')
    # q_and_a_list = [
    #     # {
    #     #     "tag":"AI",
    #     #     "patterns": ["What is AI?"],
    #     #     "answer": ["Artificial Intelligence is the simulation of human intelligence in machines."]
    #     # },
    #     {
    #         "tag":"msc-it-bggfthfhffusiness-ia-data",
    #         "patterns": ["What is ML?"],
    #         "responses": ["Machine Learning is a subset of AI that involves training algorithms on data."]
    #     },
    #     {
    #         "tag":"mseeeec-it-business-ia-data",
    #         "patterns": ["What is ML?"],
    #         "responses": ["Machine Learning is a subset of AI that involves training algorithms on data."]
    #     }
    # ]

    q_and_a_list = [
        {
            'tag': 'poissson davril',
            'patterns': ["Quels sont les avantages spécifiques de suivre la formation de Développeur Logiciel à l'école La Plateforme par rapport à d'autres programmes similaires ?"],
            'responses': ['L\'école offre des places limitées avec des frais de scolarité à 0€, une première année intensive suivie d\'une alternance enrichissante, et un réseau d\'entreprises partenaires facilitant l\'insertion professionnelle des diplômés.']
        },
        {
            'tag': 'poissson demai',
            'patterns': ["Quelles sont les compétences non techniques importantes enseignées dans le cadre de la formation de Développeur Logiciel à La Plateforme ?"],
            'responses': ['En plus des compétences techniques, l\'école met l\'accent sur la gestion de projet, le développement de micro services, la sécurité du développement, le déploiement continu, la supervision de la qualité, et les tests unitaires.']
        },
        {
            'tag': 'centralediglab',
            'patterns': ["Quels sont les objectifs de la formation MSc IT Business IA et Data ?"],
            'responses': ['La formation vise à développer une expertise en intelligence artificielle et en analyse de données, et à préparer les étudiants à des carrières en stratégie numérique et en gestion de projets IT.']
        }
    ]
    mongo_ops.add_data(q_and_a_list)

    print('-----------------fetch')
    mongo_ops.fetch_data()
