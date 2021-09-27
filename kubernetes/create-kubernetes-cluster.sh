#VMware vdisk issue solution
sudo vim /etc/multipath.conf
Add this line to the above file:
#blacklist {
#    devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st|sda)[0-9]*"
#}
sudo systemctl restart multipathd.service
sudo systemctl restart multipath-tools.service

#Kubernetes full install
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

vim /etc/docker/daemon.json # when there is a mismatch of kubelet and docker driver
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}

sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ${USER}
su - ${USER}

sudo swapoff -a
sudo nano /etc/fstab

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"

sudo apt install -y kubeadm kubelet kubectl kubernetes-cni
sudo apt-mark hold kubelet kubeadm kubectl

##Just on master node
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

#kubeadm token create --print-join-command

##Just on worker node
#kubeadm join

#Archive
#Setting up Kubernetes Cluster (Do it on every node)
sudo snap install docker
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
sudo snap disable docker
sudo snap enable docker
sudo snap install microk8s --classic --channel=1.18/stable
sudo snap refresh microk8s --classic --channel=1.19/stable
sudo snap refresh microk8s --classic --channel=1.20/stable
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
su - $USER
microk8s add-node #On Kubernetes Master
microk8s join 172.16.23.1:25000/5da90d3a4f4d023948cb9545af97cd1c #On Kubernetes Workers