import sys
sys.path.insert(0, '/opt/airflow')
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from src.messaging.producer import activate_producer
from src.messaging.producer_weather import activate_producer as ap
from src.sources.join_api import run_join



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
    schedule='0 */2 * * *',
    start_date = datetime.now() - timedelta(hours=1),
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

    def run_consumer_weather_task():
            import subprocess
            result = subprocess.run(
                ['python', '-m', 'src.messaging.consumer_weather'],
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


    task_producer_weather = PythonOperator(
        task_id='producer_task_weather',
        python_callable=ap,
        retries = 3,
        retry_delay = timedelta(seconds = 30)
    )

    task_consumer_weather = PythonOperator(
            task_id='consumer_task_weather',
            python_callable = run_consumer_weather_task
        )
    join_task = PythonOperator(
         task_id = 'joining',
         python_callable = run_join
    )



    #ветка землетрясений
    task_producer >> task_consumer  
    #ветка погоды 
    task_producer_weather >> task_consumer_weather
    [task_consumer, task_consumer_weather]>>join_task

    