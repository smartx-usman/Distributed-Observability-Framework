### Install Istio
You need to have Istio up and running. Let’s install the istio operator:

```
curl -L https://istio.io/downloadIstio | | ISTIO_VERSION=1.11.3 sh -
cd istio-1.11.3 
export PATH=$PWD/bin:$PATH
```

Now, let’s instantiate the service mesh. Istio proxies include a traceID in the 'x-b3-traceid'. Notice that you will set the access logs to inject that trace ID as part of the log message:
```bash
istioctl install --set profile=demo -y
kubectl apply -f istio-operator.yaml
```

### Deploy the sample application
Add a namespace label to instruct Istio to automatically inject Envoy sidecar proxies when you deploy your application later
```bash
kubectl create namespace bookinfo
kubectl label namespace bookinfo istio-injection=enabled
```
And now the demo application bookinfo:
```bash
kubectl apply -n bookinfo -f bookinfo.yaml
kubectl get -n bookinfo services
kubectl get -n bookinfo pods
#kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
```
### Open the application to outside traffic
To access the application through Istio, you need to configure it. It is required a Gateway and a VirtualService:
```bash
kubectl apply -f bookinfo-gateway.yaml
istioctl analyze

kubectl get svc istio-ingressgateway -n istio-system
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')

export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
echo "$GATEWAY_URL"

echo "http://$GATEWAY_URL/productpage"
```

To access the application, let’s open a tunnel to the Istio ingress gateway (the entry point to the mesh):
```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system  --address 0.0.0.0 35000:80
```
Now, you can access the application through the browser: http://your-ip-address:35000/productpage

### View the dashboard (Additional)

```bash
kubectl apply -f samples/addons
kubectl rollout status deployment/kiali -n istio-system

```