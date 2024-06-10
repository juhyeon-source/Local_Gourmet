from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from scrappers.views import RecipeScraperView
import atexit

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(scrape_recipes, IntervalTrigger(hours=24)) # 24시간 주기로 스크래핑
    scheduler.start()

    # 애플리케이션 종료 시 스케줄러 종료
    atexit.register(shutdown_scheduler)

def scrape_recipes():
    view = RecipeScraperView()
    view.get(None)
    
def shutdown_scheduler():
    scheduler.shutdown()

# # 위와 완전히 같지만 정상작동하는지 테스트 해보기 위한 코드
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# import atexit
# import logging

# # 로깅 설정
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# scheduler = BackgroundScheduler()

# def start_scheduler():
#     scheduler.add_job(test_job, IntervalTrigger(seconds=3)) # 3초 간격으로 작업 실행
#     scheduler.start()

#     # 애플리케이션 종료 시 스케줄러를 종료
#     atexit.register(shutdown_scheduler)

# def test_job():
#     result = 1 + 1
#     print(f"Test job executed, result is {result}")

# def shutdown_scheduler():
#     scheduler.shutdown()