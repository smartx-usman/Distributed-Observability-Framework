# Create vm instances
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker1 --flavor m2.small --network c62d9fb5-ebeb-4c19-837c-0882129f5918 master1
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker1 --flavor m1.medium --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker1
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker2 --flavor m2.large --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker2
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker2 --flavor m1.small --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker3
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m1.medium --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker4
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m1.small --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker5
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m1.small --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker6
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker1 --flavor m1.small --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker7
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m2.tiny --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker8
microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m2.tiny --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker9

# Create floating ip
microstack.openstack floating ip create external --floating-ip-address 10.20.20.10
microstack.openstack floating ip create external --floating-ip-address 10.20.20.11
microstack.openstack floating ip create external --floating-ip-address 10.20.20.12
microstack.openstack floating ip create external --floating-ip-address 10.20.20.13
microstack.openstack floating ip create external --floating-ip-address 10.20.20.14
microstack.openstack floating ip create external --floating-ip-address 10.20.20.15
microstack.openstack floating ip create external --floating-ip-address 10.20.20.16
microstack.openstack floating ip create external --floating-ip-address 10.20.20.17
microstack.openstack floating ip create external --floating-ip-address 10.20.20.18
microstack.openstack floating ip create external --floating-ip-address 10.20.20.19

# Assign floating ip
microstack.openstack server add floating ip master1 10.20.20.10
microstack.openstack server add floating ip worker1 10.20.20.11
microstack.openstack server add floating ip worker2 10.20.20.12
microstack.openstack server add floating ip worker3 10.20.20.13
microstack.openstack server add floating ip worker4 10.20.20.14
microstack.openstack server add floating ip worker5 10.20.20.15
microstack.openstack server add floating ip worker6 10.20.20.16
microstack.openstack server add floating ip worker7 10.20.20.17
microstack.openstack server add floating ip worker8 10.20.20.18
microstack.openstack server add floating ip worker9 10.20.20.19
