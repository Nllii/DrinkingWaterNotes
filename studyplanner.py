import time
import random
import subprocess
import os

# Define the duration of each Pomodoro session and break
WORK_DURATION = 25 * 60  # 25 minutes in seconds
BREAK_DURATION = 5 * 60  # 5 minutes in seconds

# Define the index of the current task
current_task_index = 0
TASKS = []
name_task = {}
random_task_int = [15,12,3,4,5,6,7,8,9,10,11,12,13,14,15]


TASK = [
    "Read WHO guide on water chlorination: https://www.who.int/water_sanitation_health/publications/chlorination/en/",
    "Watch AWWA video on basics of chlorination: https://www.youtube.com/watch?v=IeYoxX5HNV0",
    "Read EPA article on chlorine disinfection: https://www.epa.gov/ground-water-and-drinking-water/chlorine-disinfection-drinking-water",
    "Read EPA guidance manual on chlorination: https://www.epa.gov/sites/default/files/2014-06/documents/chlorination-guidance-manual.pdf",
    "Watch IWA video on benefits and drawbacks of chlorination: https://www.youtube.com/watch?v=JJjxeytfUY8",
    "Review AWWA case study on use of chlorination in a water treatment plant: https://www.awwa.org/Portals/0/AWWA/ETS/Resources/CaseStudies/Chlorination.pdf",
    "Read ACS article on history of water chlorination: https://www.acs.org/content/acs/en/education/resources/highschool/chemmatters/past-issues/2018-2019/december-2018/the-history-of-water-chlorination.html",
    "Watch WHO video on different types of chlorine used in water treatment: https://www.youtube.com/watch?v=PsR62tGwDxk",
    "Review research paper on effectiveness of chlorination in removing pathogens in water: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3284092/"
]


# for json reasons... Append the task "name" to the task object
task_int = random.choices(random_task_int, k=len(TASK))
for i in range(len(TASK)):
    # {"name": "Read WHO guide on water chlorination:", "duration": 60*30},
    name_task['name'] = TASK[i]
    name_task['duration'] = 60*int(task_int[i])
    TASKS.append(name_task)
    
    


def send_notification(title, message, sound=None, actions=None, close_label=None, reply=False, dropdown_label=None,timeout=None,open_url=None):
    """Send a notification using the macOS `alerter`  or terminal-notifier command.
    Of course only works on macOS.
    
    """
    isMacOS = os.uname().sysname == "Darwin"
    if not isMacOS: 
        return
    command = ['terminal-notifier', '-title', title, '-message', message]
    if sound:
        command.extend(['-sound', sound])
    if actions:
        actions_list = ','.join(actions)
        command.extend(['-actions', actions_list])
    if close_label:
        command.extend(['-closeLabel', close_label])
    if reply:
        command.append('-reply')
    if dropdown_label:
        command.extend(['-dropdownLabel', dropdown_label])
    if timeout:
        command.extend(['-timeout', timeout])
    if reply:
        command.append('-json')
    # -open 'https://www.youtube.com/watch?v=IeYoxX5HNV0'
    if open_url:
        command.extend(['-open', open_url])
    
    
    subprocess.Popen(command)



def return_url():
    transferProtocol = TASKS[current_task_index]["name"].split(":")[1].strip()
    url_path = TASKS[current_task_index]["name"].split(":")[2].strip()
    url = transferProtocol + ":" + url_path
    return url

while True:
    # Start a Pomodoro work session
    task_name = TASKS[current_task_index]["name"]
    task_duration = TASKS[current_task_index]["duration"]
    url = return_url()
    print(f"Work on '{task_name}' for {task_duration/60} minutes")
    start_time = time.time()
    end_time = start_time + task_duration
    send_notification(title="Study Planner", message=f"Work on \n'{task_name}' \nfor {task_duration/60} minutes", sound="default", actions=["OK"], close_label="OK", reply=True, dropdown_label=None,timeout=None,open_url=url)
    while time.time() < end_time:
        remaining_time = round(end_time - time.time())
        print(f"Time remaining: {remaining_time // 60} minutes {remaining_time % 60} seconds" , end="\r")
        time.sleep(1)

    # Take a break
    print(f"Take a break for {BREAK_DURATION/60} minutes", end="\n")
    time.sleep(BREAK_DURATION)

    # Move on to the next task
    current_task_index += 1
    if current_task_index == len(TASKS):
        current_task_index = 0

