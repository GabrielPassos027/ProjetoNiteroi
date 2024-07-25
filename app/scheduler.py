from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.anp_controller import save_anp_data
from app.controllers.focus_controller import save_focus_data
from app.controllers.ibge_controller import save_ipca_ibge_data, save_desemprego_ibge_data, save_caged_data_to_db
from app.controllers.siconfi_controller import fetch_siconfi_RREO_data, fetch_siconfi_RGF_data

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    
    # Agendar a tarefa para ser executada no quinto dia de cada mês às 00:00
    scheduler.add_job(func=lambda: save_anp_data(app), trigger="cron", day=5, hour=0, minute=0)
    
    scheduler.add_job(func=lambda: save_focus_data(app), trigger="cron", day=5, hour=0, minute=0)
    
    scheduler.add_job(func=lambda: save_ipca_ibge_data(app), trigger="cron", day=5, hour=0, minute=0)

    scheduler.add_job(func=lambda: save_desemprego_ibge_data(app), trigger="cron", day=5, hour=0, minute=0)    
    
    scheduler.add_job(func=lambda: save_caged_data_to_db(app), trigger="cron", day=5, hour=0, minute=0)

    
    
    
    #scheduler.add_job(func=lambda: fetch_siconfi_RREO_data(app), trigger="interval", minutes=1)
     
    print("Jobs iniciadas com sucesso!")
    scheduler.start()