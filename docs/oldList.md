```python
def list():

    work = [
        {
            "name": "Dipisha",
            "description": "Dipisha is my sister which is very important to me, so here goal is mine goal."
        },
        {
            "name": "Orca",
            "description": "Orca is a cyptro bot which is crucial project for me to pull off."
        },
        {
            "name": "Delicious",
            "description": "Delicious is a online dating application. Which is very important to me to enhance my skills."
        },
        {
            "name": "Interview-prep",
            "description": "Doing DSA and system design for interview preparation."
        },
        {
            "name": "Shadana",
            "description": "Shadana is a flutter project for nepal students"
        },
        {
            "name": "Potpie",
            "description": "Potpie is open source project for making agents"
        }
    ]

    for task in work:
        id = str(uuid4())
        a = Work(id=id, name=task["name"], description=task["description"])
        session.add(a)
        session.commit()


    wanna_be = [
        {
            "name": "Cleaner Deepesh",
            "description": "Cleaner Deepesh is a goal to keep my room clean."
        },
        {
            "name": "Space Explorer Deepesh",
            "description": "Space Explorer Deepesh is a goal to learn about space."
        },
        {
            "name": "Excerise Deepesh",
            "description": "Excerise Deepesh is a goal to play sports."
        },
        {
            "name": "Runner Deepesh",
            "description": "Runner Deepesh is a goal to run daily."
        },
        {
            "name": "Speaker Deepesh",
            "description": "Speaker Deepesh is a goal to speak in public."
        },
        {
            "name": "Money Manager Deepesh",
            "description": "Money Manager Deepesh is a goal to manage money."
        },
        {
            "name": "Handsome Deepesh",
            "description": "Handsome Deepesh is a goal to look handsome."
        }
    ]

    for task in wanna_be:
        id = str(uuid4())
        b= WannaBe(id=id, name=task["name"], description=task["description"])
        session.add(b)
        session.commit()

    
    hobby = [
        {
            "name": "Volleyball",
            "description": "I am wanted to contribute to volleyball as the hobby."
        },
        {
            "name": "Chess",
            "description": "I am wanted to play chess as the hobby."
        },
        {
            "name": "Writing",
            "description": "I am wanted to write as the hobby."
        },
        {
            "name": "Cyptro",
            "description": "I am wanted to learn about cyptro as the hobby."
        },
        {
            "name": "History Philosophy and Religion",
            "description": "I am wanted to read about history as the hobby."
        }, 
        {
            "name": "Anime",
            "description": "I am wanted to watch anime as the hobby."
        },
        {
            "name": "Food",
            "description": "I am wanted to learn and how to eat food as the hobby."
        },
        {
            "name" : "Travel",
            "description": "I am wanted to go out travel take many photograph as the hobby."
        }
    ]

    for task in hobby:
        id = str(uuid4())
        c= Hobby(id=id, name=task["name"], description=task["description"])
        session.add(c)
        session.commit()
```