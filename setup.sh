python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp printmanager.service /etc/systemd/system/printmanager.service
systemctl daemon-reload
ln -sf printmanager-ssl.conf /etc/apache2/sites-enabled/printmanagerssl.conf
systemctl start printmanager
systmectl enable printmanager
systemctl restart apache2