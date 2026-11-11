"""Log benchmark evidence to a configured MLflow tracking server. No fake metrics."""
import json, pathlib, os
def log_results(results_file="evals/results/benchmark.json"):
    import mlflow
    runs=json.loads(pathlib.Path(results_file).read_text())
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT","lsk-agent-pilot"))
    with mlflow.start_run(run_name=os.getenv("PROMPT_VERSION","v1")):
        mlflow.log_params({"prompt_version":os.getenv("PROMPT_VERSION","v1"),"model_name":os.getenv("MODEL_NAME","unconfigured"),"dataset_version":"synthetic-v1"})
        valid=[x for x in runs if "error" not in x]
        mlflow.log_metric("case_count",len(runs))
        mlflow.log_metric("request_success_rate",len(valid)/max(1,len(runs)))
        mlflow.log_metric("source_recall_proxy",sum(x.get("citation_hit",False) for x in valid)/max(1,len(valid)))
        if valid:mlflow.log_metric("mean_latency_seconds",sum(x["latency_seconds"] for x in valid)/len(valid))
        mlflow.log_artifact(results_file)
if __name__=="__main__":log_results()
