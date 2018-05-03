# -*- mode: ruby -*-
# vi: set ft=ruby :

###### SJB (See David) https://github.com/lindes/tutorials/blob/master/vagrants/flask/Vagrantfile
# We can use either python 2 or python 3.  If you want python 3, set
# want_python_3 to true instead of false.  Note that you'll also have to
# do a "vagrant destroy" and another "vagrant up" to get the change to
# take hold.
want_python_3=true

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  #### SJB Change all ubuntu accept this one - this doesnot change as it is the name of the vm.box
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  ###### SJB change fall back = True ... (See David) https://github.com/lindes/tutorials/blob/master/vagrants/flask-py3/Vagrantfile 
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 5000, host: 5000, auto_correct: true

  ###### SJB added path configuation for ubuntu ... (See David) https://github.com/lindes/tutorials/blob/master/vagrants/flask-py3/Vagrantfile
  ###### Changed "/home/ubuntu/src" to "/home/vagrant/src" - rerout 
  # This puts the current directory (where this Vagrantfile is) from
  # the "host" computer (the Mac or Windows (or Linux) box you're
  # physically sitting in front of) under what's at ~/src on the
  # "guest" -- i.e. the virtual machine, i.e. once you're ssh'd into
  # vagrant.  Anything you put in ~/src/ within the guest will show up
  # in the current directory on the host, and vice versa.
  config.vm.synced_folder ".", "/home/vagrant/src"

  ##### SJB Provisioning:

  ##### SJB ttyname - Early user terminals connected to computers were 
  ##### electromechanical teleprinters or teletypewriters (TeleTYpewriter, TTY), 
  ##### and since then TTY has continued to be used as the name for the text-only 
  ##### console although now this text-only console is a virtual console not a physical console.
  ##### (See David) https://github.com/lindes/tutorials/blob/master/vagrants/flask-py3/Vagrantfile
  # because I'm tired of getting errors that say:
  # "mesg: ttyname failed: Inappropriate ioctl for device"
  # See https://superuser.com/a/1277604/57367 for more info.
  config.ssh.shell="bash"

  ###### SJB (See David) https://github.com/lindes/tutorials/blob/master/vagrants/flask-py3/Vagrantfile 
  # some provisioning to install the software we'll be using:
  # apt (is look up man apt) 
  # .profile - A (very) quick primer on .bash_profile for Mac Users. There is a hidden file in your 
    # Mac's user directory named .bash_profile. This file is loaded before Terminal loads your shell 
    # environment and contains all the startup configuration and preferences for your command line interface
  p3 = want_python_3 ? '3' : ''
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get -y full-upgrade

    # feel free to add more software, e.g. postgresql or whatever
    apt-get install -y python#{p3}-pip postgresql libssl-dev redis-server
    
    pip#{p3} install --upgrade pip
    
    pip install -r /home/vagrant/src/requirements.txt

    echo "export FLASK_APP=/home/vagrant/src/server.py" >> ~vagrant/.profile
    echo "export FLASK_DEBUG=1" >> ~vagrant/.profile
    echo "export VAGRANT_DIR='#{Dir.pwd.sub(Dir.home, "~")}'" >> ~vagrant/.profile
    # if you need to run a seed.py or something, this might be a good
    # place to add that.
  SHELL

  ###### SJB (See David) https://github.com/lindes/tutorials/blob/master/vagrants/flask-py3/Vagrantfile 
  # The following /could/ be shortened to basically just the sudo
  # command, but I find it nice to be able to report status, and type
  # 'vagrant up' potentially-repeatedly without worrying that it'll
  # kill the flask server, but also that it'll try to start flask if
  # it it's not running:
  # lsof = list open files
  # lsof -i (select the listing of files any of whose internet addsess matches address specified)
  # sudo (sudo attempts to change to that user's home directory before running shell) -u (is user) ubuntu 
  # -i (is login) -n(is non-interactive. avoid proption user for input) flask run -h (is host) 0 (is ?)
  # -p ( prompt ? port?)
  config.vm.provision "shell", run: "always", inline: <<-SHELL
    # look for flask  which is actually listening:
    if lsof -i | grep python3
    then
      # note: this will also print out the lsof info with the (guest) port number.
      echo "Looks like flask is already running!  Woohoo!"
    else
      # start a new flask:
      echo "Flask doesn't seem to have been running; we'll try to start one."
      (sudo -u vagrant -i -n flask run -h 0 -p 5000 2>&1 | logger -plocal0.info -t flask.run) &
      sleep 5       # this *seems* to be all it takes, but maybe not always.
      if lsof -i | grep python3
      then
        echo "Sweet, looks like it's up now. :)"
      else
        echo "Hmm... may not have worked; might need to investigate?" >&2
      fi
      # don't check it, just continue
    fi
  SHELL

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
