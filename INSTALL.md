#### Python installation
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6

#### Installing virtual environment
cd ~
python3.6 -m venv virtualenv --without-pip
cd virtualenv/
source bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python3

#### Installing pip for venv
pip install pipenv==2018.6.25
pip install pip==18.0
pipenv install

