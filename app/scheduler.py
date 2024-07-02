from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.anp_controller import save_anp_data
from app.controllers.focus_controller import save_focus_data

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    
    # Agendar a tarefa para ser executada no quinto dia de cada mês às 00:00
    scheduler.add_job(func=lambda: save_anp_data(app), trigger="cron", day=5, hour=0, minute=0)
    
    # scheduler.add_job(func=lambda: save_focus_data(app), trigger="cron", day=5, hour=0, minute=0)
    scheduler.add_job(func=lambda: save_focus_data(app), trigger="interval", minutes=2)
    print("Jobs iniciada com sucesso!")
    scheduler.start()