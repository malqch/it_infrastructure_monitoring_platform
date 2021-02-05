#!/bin/bash
#项目的目录
SERVICE_DIR=/home/rock/quality_inspection/python-workspace/project_monitor
#项目的名字
SERVICE_NAME=project_monitor
#gunicorn的配置文件名
SERVICE_CONF=gunicorn_config.py
#虚拟环境的路径
VIRTUAL_DIR=/home/rock/anaconda3/envs/venv/bin
#source activate venv
cd $SERVICE_DIR
$VIRTUAL_DIR/gunicorn $SERVICE_NAME.wsgi:application -c $SERVICE_CONF
echo `ps -ef | grep -w "$SERVICE_NAME"|grep -v "grep"|awk '{print $2}'`
echo "*** start $SERVICE_NAME ***"