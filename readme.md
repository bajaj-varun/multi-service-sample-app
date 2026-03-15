# Multiple Service deployed independently 

The purpose of this application is to deploy multiple services independent to each other and developer can focus only on portion of code which they are responsible without worrying and knowledge of other services.

1. Service Independence & Celery Isolation: We have transformed App1, App2, and App3 into entirely separate Flask + Celery applications. Each application has:

- A `requirements.txt`,`app.py`, and `tasks.py`.
- Their own `Dockerfile` separating their execution environment.
- Separate backend queues configured using different database indexes in Redis (e.g., `redis://redis.../1, redis://redis.../2, redis://redis.../3)`.
- Independent Kubernetes deployments and worker replicas (configured in AppX/deployment.yaml).

2. A 2-Worker Kind Cluster Configuration: I've created a configuration file for your kind cluster at 

- `infrastructure/kind-config.yaml` explicitly defining two separate computing worker nodes as requested:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```
3. App3 Calling App2: In App3 development, we implemented the `call_app2_health_check`
 endpoint using the Kubernetes internal DNS identifier `(app2.default.svc.cluster.local)` provided to the application using an environment variable `(APP2_URL)`. This allows testing the app from outside the cluster natively utilizing port-forwarding while letting it effortlessly resolve when inside the cluster.

```python
# App3/src/app.py
APP2_URL = os.environ.get("APP2_URL", "http://app2.default.svc.cluster.local:5002")
@app.route('/call_app2_health_check')
def call_app2_health_check():
    response = requests.get(f'{APP2_URL}/health_check', timeout=5)
    return jsonify({"app2_response": response.json(), "status": "Success"})
```
<br/>

## How to deploy the entire environment
I've generated a fast-deployment bash script for you. Run this directly from your hello-world directory:

```bash
./deploy.sh
```
<br/>
This script will automatically:

1. Spin up the `kind` cluster using the requested 2-worker configuration.
2. Build the independent Docker images for `app1`, `app2`, and `app3`.
3. Load those images explicitly into your local kind cluster.
4. Deploy the shared Redis infrastructure and the 3 distinct application components to your cluster.
</br>

## How you can develop App3 independently
Once your cluster is completely up and running, here is how you manage a developer workflow focusing purely on `App3`:

1. <b>Open a local port to App2 from your cluster</b>: If you want your local `App3` instance to communicate with the `App2` inside your cluster without deploying, create a persistent port-forward channel:

```bash
kubectl port-forward svc/app2 5002:5002
```
</br>
2. <b>Run your local App3 codebase</b>: In a separate terminal, export the environment variable so it targets your local port-forwarding rather than the kubernetes internal mesh framework:

```bash
cd App3/src
export APP2_URL="http://127.0.0.0:5002"
flask --app app.py run --port=5003
```
</br>

Now, any changes you make within App3 can be tested instantly without rebuilding your containers or cluster every time!