Objective: to connect to multiple raspberry pi zero devices at once from a single computer by statically assigning IP addresses.

This document assumes you can already connect to the raspberry pi 0 using ssh.

ssh-keyscan 192.168.2.1 > ~/.ssh/known_hosts

On your computer youre using to connect to the Pi, run "ipconfig" (or "ifconfig" on Mac OS or linux)
Make note of you IP version 4 address, subnet mask, and default gateway for the network card connecting to your raspberry pi (it may be called "bridge100" on mac/linux. May be called a different name on Windows) 
Ex:
"bridge100: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=3<RXCSUM,TXCSUM>
	ether a6:5e:60:dd:2c:64 
	inet 192.168.2.1....""

Connect to Raspberry Pi Zero using the hostname (ex. ssh pi@raspberrypi.local)

enter the command "sudo su -" to change to the "superuser" known as root (this gives us rights to change network settings)

change to the folder "etc" by entering: "cd /etc"

edit the file dhcpcd.conf using nano:
"nano dhcpcd.conf"

insert the following lines of code in a blank space:
interface usb0
static ip_address=192.168.2.8/24
static router=192.168.2.1/24
static domain_name_servers=192.168.2.1

NOTE: make sure the static ip address here is in the same network as the interface we made note of earlier. For example:
-Mac interface connecting to the Pi: 192.168.2.1
-IP address of the usb0 network interface on the Pi: 192.168.2.5
...where the 2 represents which network the devices reside on.

Exit the nano text edit by performing ctrl-o, ENTER, ctrl-x.

Restart the network service to apply the changes: service networking restart

enter "exit" twice to logout of the raspberry pi.

Now attempt to ssh into the Pi with the newly set ip address of 192.168.2.5
