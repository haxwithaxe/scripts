#!/bin/bash

# Macro like functions to simplify iptables config
# Assumes Debian or similar distro

# source this file and use the functions defined below.
usage(){
	cat - <<EOU
functions:
	enable_ip_forward
	install_ipt_persistent
	forward_both
	forward_tcp
	forward_udp
	clear_rules
	set_default_policies
	protect_local_services
	allow_default_ssh
	drop_priv_ports
	setup_NAT
	save_iptables
	init_router
EOU
}

# -e fail early
# -x say exactly what is being done
set -ex

WAN=<wan dev>
LAN=<lan dev>

LAN_NET=192.168.0.0
LAN_MASK=255.255.255.0

ssh_port=22

### Helper Functions

# Enable IP forwarding
enable_ip_forward(){
	cat - >/etc/sysctl.d/local.conf <<EOF
net.ipv4.conf.default.rp_filter=1
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
EOF
	sysctl --system
}

# Install required package
# Debian-like distro dependent
install_ipt_persistent(){
	apt-get install iptables-persistent
}

# Forward both UDP and TCP
# from port ($1) to dest ip[:port] ($2)
forward_both(){
	dport=$1
	dest=$2
	forward_tcp
	forward_udp
}

# Forward TCP
# from port ($1) to dest ip[:port] ($2)
forward_tcp(){
	dport=${dport:-$1}
	dest=${dest:-$2}
	iptables -t nat -A PREROUTING -p tcp --dport $dport -i ${WAN} -j DNAT --to $dest
}

# Forward UDP
# from port ($1) to dest ip[:port] ($2)
forward_udp(){
	dport=${dport:-$1}
	dest=${dest:-$2}
	iptables -t nat -A PREROUTING -p udp --dport $dport -i ${WAN} -j DNAT --to $dest
}

# Clear all rules
clear_rules(){
	/etc/init.d/iptables-persistent flush
}

# Set default policies
set_default_policies(){
	clear_rules
	iptables -P INPUT ACCEPT
	iptables -P OUTPUT ACCEPT
	iptables -P FORWARD DROP
}

# Lockdown services to the LAN
protect_local_services(){
	iptables -I INPUT 1 -i ${LAN} -j ACCEPT 
	iptables -I INPUT 1 -i lo -j ACCEPT
	iptables -A INPUT -p UDP --dport bootps ! -i ${LAN} -j REJECT
	iptables -A INPUT -p UDP --dport domain ! -i ${LAN} -j REJECT
}

# Allow SSH to router
allow_default_ssh(){
	iptables -A INPUT -p TCP --dport ${ssh_port} -i ${WAN} -j ACCEPT
}

# Drop TCP and UDP to privlidged ports (why?)
drop_priv_ports(){
	# Drop TCP
	iptables -A INPUT -p TCP ! -i ${LAN} -d 0/0 --dport 0:1023 -j DROP
	# Drop UDP
	iptables -A INPUT -p UDP ! -i ${LAN} -d 0/0 --dport 0:1023 -j DROP
}

# Setup NAT
setup_NAT(){
	# Drop Forwards from LAN iface->LAN
	iptables -I FORWARD -i ${LAN} -d ${LAN_NET}/${LAN_MASK} -j DROP 
	# Forward LAN->LAN
	iptables -A FORWARD -i ${LAN} -s ${LAN_NET}/${LAN_MASK} -j ACCEPT
	# Forward WAN->LAN
	iptables -A FORWARD -i ${WAN} -d ${LAN_NET}/${LAN_MASK} -j ACCEPT
	# Enable NAT
	iptables -t nat -A POSTROUTING -o ${WAN} -j MASQUERADE
	# make sure we can get back in right away
	allow_default_ssh
}

# Save rules for reload on boot
# Debian-like distro dependent
save_iptables(){
	/etc/init.d/iptables-persistent save
}

### End Helper Functions

# setup all default configs
# for initial setup or redo
init_router(){
	default_policies
	protect_local_services
	drop_priv_ports
	setup_NAT
	save_iptables
}

