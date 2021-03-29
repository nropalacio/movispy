from apscheduler.schedulers.background import BackgroundScheduler
from .something_update import update_something, printHello
from .scrips.updatedrive import iniciar

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_something,'interval', minutes=5)
    scheduler.start()
    
def drive():
    scheduler = BackgroundScheduler()
    scheduler.add_job(iniciar,'interval', hours=2)
    scheduler.start()
    