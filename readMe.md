▶️Currently is setup with a Postgres Datase
▶️The Data base configs are using an alias file for it's connection, you will have to add a .env file that has this similar structure to connect to a postgress DB: 

SECRET_KEY=django-insecure-728k0bs%91o$^sp%aa_ji@2fmtwpdk7r1na#*$%l2+%)7tnpo3
DB_NAME= **your Name for DB**
DB_USER=**The login for your DB**
DB_PASSWORD=**Your DB password for that login**
DB_HOST=**The address your postgres DB is at**
DB_PORT=**Default port is 5432, if not using default port change here**