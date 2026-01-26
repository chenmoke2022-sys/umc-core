"""
Airflow DAG template (optional)

This file is a template only. It demonstrates DAG thinking for ML pipelines:
data checks -> train -> eval -> registry -> evidence artifacts.

It is intentionally not required to run the toy example.
"""

from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
except Exception:  # pragma: no cover
    DAG = None
    BashOperator = None


def build_dag():
    if DAG is None:
        raise RuntimeError("Airflow is not installed. This file is a template only.")

    with DAG(
        dag_id="mlops_pipeline_toy",
        start_date=datetime(2026, 1, 1),
        schedule_interval=None,
        catchup=False,
        tags=["toy", "mlops", "evidence-pack"],
    ) as dag:
        run = BashOperator(
            task_id="run_pipeline",
            bash_command="python examples/mlops_pipeline_toy/run.py --out examples/mlops_pipeline_toy/artifacts",
        )
        env = BashOperator(
            task_id="collect_env",
            bash_command="python tools/collect_env.py --out examples/mlops_pipeline_toy/artifacts/env.json",
        )
        manifest = BashOperator(
            task_id="make_manifest",
            bash_command="python tools/make_manifest.py --dir examples/mlops_pipeline_toy/artifacts --out examples/mlops_pipeline_toy/artifacts/manifest.json",
        )
        validate = BashOperator(
            task_id="validate",
            bash_command="python tools/validate_artifacts.py --artifacts examples/mlops_pipeline_toy/artifacts",
        )
        run >> env >> manifest >> validate
        return dag


if DAG is not None:  # pragma: no cover
    dag = build_dag()


