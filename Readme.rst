Create a virtual environment

    Recommended python version: 3.6.9

Steps to install mysql in django

    sudo apt install python3-dev
    sudo apt install python3-dev libmysqlclient-dev default-libmysqlclient-dev
    pip install mysqlclient

Steps to set up mysql database locally

    sudo mysql -u root
    create database wallet_application;
    CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY '123@Test';
    GRANT ALL ON wallet_application.* TO 'djangouser'@'%';
    FLUSH PRIVILEGES;

pip3 install -r requirements.txt
