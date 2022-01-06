rm -rf *.pid
export PYTHONOPTIMIZE=1
celery multi start w1 -A monitor_server -l info --logfile=logs/celery-worker.log --pidfile=celery-worker.pid
celery -A monitor_server beat -l info >  logs/celery-beat.log  2>&1  &
