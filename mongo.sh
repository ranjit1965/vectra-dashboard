chmod 777 mongo.sh
pip install -r requirements.txt
mkdir composs
cd composs
sudo dnf install -y https://repo.mongodb.org/yum/redhat/8/mongodb-org/4.4/x86_64/RPMS/mongodb-org-server-4.4.6-1.el8.x86_64.rpm
sudo systemctl start mongod
sudo systemctl enable mongod

wget https://downloads.mongodb.com/compass/mongodb-compass-1.43.5.x86_64.rpm
sudo yum install mongodb-compass-1.43.5.x86_64.rpm -y

mongodb-compass --no-sandbox
