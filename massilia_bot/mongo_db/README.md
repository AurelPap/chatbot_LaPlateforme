## Usage :

from mongo_operations import MongoOperations
with MongoOperations() as mongo_ops:
    print('-----------------delete all data from the db, use carefully')
    mongo_ops.delete_data()
    print('-----------------reset the db with the specified json files, use carefully')
    mongo_ops.reset_data()

    print('-----------------add New tags with associated patterns and answer to the db')
    q_and_a_list = [
        {
            "tag":"AI",
            "patterns": ["What is AI?"],
            "answer": ["Artificial Intelligence is the simulation of human intelligence in machines."]
        },
        {
            "tag":"msc-it-business-ia-data",
            "patterns": ["What is ML?"],
            "answer": ["Machine Learning is a subset of AI that involves training algorithms on data."]
        }
    ]
    mongo_ops.add_data(q_and_a_list)

    print('-----------------fetch all datas from the db and return the content of the json file')
    mongo_ops.fetch_data()


## Notes

- Add Data ne permet pas de rajouter des données à un tag existant pour le moment, cela permet uniquement de rajouter de nouveaux tags pour l'heure.
Reset
- Le fichier constants.py contient les variables nécessaires à la connextion à l'app et à l'utilisation du script
- - Si le fichier json est dans le même dossier que le script, laisser le PATH vide (""), autrement en spécifier un sans le nom du fichier qui se trouve dans la constante FILENAME
