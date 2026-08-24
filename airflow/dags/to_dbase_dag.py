import sys
sys.path.insert(0, '/opt/airflow')
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from src.messaging.producer import activate_producer



default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
}


with DAG(
    dag_id='data_transfer_dag',
    default_args=default_args,
    schedule='@daily',
    start_date=datetime.now(),
    catchup=False,
    max_active_runs=1,
) as dag:
    
    task_producer = PythonOperator(
        task_id='producer_task',
        python_callable=activate_producer
    )
    
    task_consumer = BashOperator(
        task_id='consumer_task',
        bash_command='python -m src.messaging.consumer'
    )
    
    task_producer >> task_consumer