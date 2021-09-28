# Setting up Kubernetes Dashboard
These are the instructions to how to set up Kubernetes dashboard that is accessible from outside your cluster. 

### Generate Certificate by Executing the Following Commands
First, add the actual IP of Kubernetes master to the file san.cnf field IP.1.
```shell
sudo mkdir /certs    
sudo chmod 777 -R /certs
openssl req -out /certs/dashboard.csr -newkey rsa:2048 -nodes -keyout /certs/dashboard.key -config san.cnf
openssl x509 -req -sha256 -days 3650 -in /certs/dashboard.csr -signkey /certs/dashboard.key -out /certs/dashboard.crt -extensions req_ext -extfile san.cnf
sudo chmod 777 -R /certs
```

### Deploy Kubernetes Dashboard 
```shell
kubectl apply -f kubernetes-dashboard/kubernetes-dashboard.yml
```

### Create Service Account
```shell
kubectl apply -f kubernetes-dashboard/serviceaccount.yml
```

### Create RBAC
```shell
kubectl apply -f kubernetes-dashboard/rbac.yml
```

### Generate Access Token
```shell
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
```

### Access the Dashboard Web URL with Generated Token
https://ip:31000