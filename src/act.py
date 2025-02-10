import random
import click
@click.command()
def main():

    regular_task_list = [

    "Going to gym",
    "Caring Yourself"
    ]



    wanna_deepesh_list = [
    "Cleaner Deepesh", 
    "Space Explorer Deepesh",
    "Foddy Deepesh",
    "Traver Deepesh",
    "Anime Deepesh",
    "Sports Deepesh",
    "Runner Deepesh",
    "Speaker Deepesh",
    "Money Manager Deepesh",
    "Writer Deepesh",
    "Handsome Deepesh",
    ]

    task_deepesh = [
    "sister",
    "orca",
    "delicious",
    "interview-prep",
    "shadana",
    "potpie",
    ]
#TODO: Future task
    wanna_be_task = [
    "learning-backend",
    "friend-time",
    "system-desing",
    "mother-walking"
    ]   

    quote_task = [
    "kidness",
    "words"
    ]

    number_of_task = 2

    quote_task_result = random.choice(quote_task)

    if (quote_task_result == "words"):
        print("Never go back from your words")

    elif (quote_task_result == "kidness"):
        print("Today is alone time")

# majar task 

    task_deepesh_result = random.choice(task_deepesh)

    print(f"solve the issue of this task {task_deepesh_result} and move to next task")


# diplomatic task

    result = random.randint(1, number_of_task)

    if (result == 1):
        task_deepesh_result = random.choice(task_deepesh)
        print(f"this is diplomatic task {task_deepesh_result} no code just help and gather information")
    else: 
        task_wanna_deepesh_result = random.choice(wanna_deepesh_list)

        print(f"this day diplomatic task { task_wanna_deepesh_result} complete and you will be wanna be deepesh")

if __name__ == "__main__":
    main()
