import redis
from conf import REDIS_CONF
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

bonus_redis = redis.Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=REDIS_CONF['db'])

jobs_key = 'collection_api_apscheduler.jobs'

run_times_key = 'collection_api_apscheduler.run_times'

job_stores = {
    'default': RedisJobStore(jobs_key=jobs_key, run_times_key=run_times_key, **REDIS_CONF)
}

executors = {
    'default': {'type': 'threadpool', 'max_workers': 20}
}

job_defaults = {
    'coalesce': True, # 相同任务同时触发多次时，只运行一次
    'max_instances': 3,
    # 'misfire_grace_time': 30, # 过期30秒依然执行该任务
}

scheduler = BackgroundScheduler(jobstores=job_stores, executors=executors, job_defaults=job_defaults)
scheduler.start()
