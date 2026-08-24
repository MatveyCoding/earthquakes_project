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
    def run_consumer_task():
        import subprocess
        result = subprocess.run(
            ['python', '-m', 'src.messaging.consumer'],
            capture_output=True,
            text=True,
            cwd='/opt/airflow'
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            raise Exception(f"Exit code: {result.returncode}")

    task_consumer = PythonOperator(
        task_id='consumer_task',
        python_callable=run_consumer_task
    )

    
    task_producer >> task_consumer


    