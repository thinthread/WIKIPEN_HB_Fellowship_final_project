# -*- mode: ruby -*-
# vi: set ft=ruby :

###### SJB 
want_python_3=true


Vagrant.configure("2") do |config|

  #### SJB 
  config.vm.box = "ubuntu/xenial64"

  ###### SJB 
  config.vm.network "forwarded_port", guest: 5000, host: 5000, auto_correct: true

  ###### SJB 
  config.vm.synced_folder ".", "/home/vagrant/src"

  ##### SJB Provisioning:
  config.ssh.shell="bash"

  ###### SJB 
  p3 = want_python_3 ? '3' : ''
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get -y full-upgrade

    # feel free to add more software, e.g. postgresql or whatever
    apt-get install -y python#{p3}-pip postgresql postgresql-contrib libssl-dev redis-server libpq-dev
    
    pip#{p3} install --upgrade pip
    
    pip#{p3} install -r /home/vagrant/src/requirements.txt

    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
    wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -

    echo "export FLASK_APP=/home/vagrant/src/server.py" >> ~vagrant/.profile 
    echo "export FLASK_DEBUG=1" >> ~vagrant/.profile
    echo "export VAGRANT_DIR='#{Dir.pwd.sub(Dir.home, "~")}'" >> ~vagrant/.profile

    # if you need to run a seed.py or something, this might be a good
    # place to add that.
    sudo -u postgres psql <<EOF
      CREATE USER vagrant;
      CREATE DATABASE pens;
      GRANT ALL ON DATABASE pens TO vagrant;
EOF

    sudo -u vagrant python3 /home/vagrant/src/model.py

    psql pens


  SHELL

  ###### SJB 
  config.vm.provision "shell", run: "always", inline: <<-SHELL
    # look for flask  which is actually listening, in this case flask is seen as python3 actually gunicorn:
    if lsof -i | grep gunicorn
    then
      # note: this will also print out the lsof info with the (guest) port number.
      echo "Looks like flask is already running!  Woohoo!"
    else
      # start a new flask:
      echo "Flask doesn't seem to have been running; we'll try to start one."

      # Hmmmmmm need to change this, how to run Flask but also Gunicorn.
      # Can't run/ show DB till streaming is reinstated.
      sudo -u vagrant -i -n gunicorn server:app --worker-class gevent --bind 0.0.0.0:5000 --reload-engine poll --graceful-timeout 30 --chdir /home/vagrant/src --daemon --log-syslog
      sleep 1       # this *seems* to be all it takes, but maybe not always.
      
      if lsof -i | grep gunicorn
      then
        echo "Sweet, looks like it's up now. :)"
      
      else
        echo "Hmm... may not have worked; might need to investigate?" >&2
      fi
      # don't check it, just continue
    fi
  SHELL
end
