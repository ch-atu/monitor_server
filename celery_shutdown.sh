ps auxww | grep 'celery'|grep 'monitor_server' | awk '{print $2}' | xargs kill -9
