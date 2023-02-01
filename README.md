# Introduce our group

Group Member:
Xiaoxi Celia Lyu,
Chihui Shao,
Quan Wang,
Kaichao Chang

Name of our team: Awesome Group :)

# Introduce our project
Project option: Mini-Amazon (standard option) 

Link to our gitlab/github repository:
https://github.com/Kaichao-Chang/CS516-Awesome-Group

Link to our group presentation:
https://www.youtube.com/watch?v=tXKEoZnoYfo

Who is working on which component:  
Xiaoxi Lyu - Users Guru (responsible for Account / Purchases)  
Chihui Shao - Products Guru (responsible for Products / Cart)  
Kaichao Chang - Sellers Guru (responsible for Inventory / Order Fulfillment)  
Quan Wang - Social Guru (responsible for Feedback / Messaging)

# Instruction on how to set up the environment and run code

Install postgresql.  
```sh
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Make sure that the postgresql service is started.   
```
sudo service postgresql start
```

```sh
cd mini-amazon-skeleton
```

Run install.sh. It should ask you to set the password of DB user.  
```sh
bash install.sh
```

Create the basic tables with postgres user. This does NOT create the "cs516" user, you will need to create one by yourself.  
```sh
sudo -u postgres bash db/setup.sh
```

Log in with postgres and start psql.  
```sh
sudo su postgres
psql
```

You should see the database `amazon` was created, with  
```sh
\l
```

There should only be one user named postgres when checking with  
```sh
\du 
```

Create the user cs516 and set password.
WITH PASSWORD '[THE PASSWORD YOU SET IN STEP 3]'
```sh
CREATE USER cs516
ALTER ROLE cs516 
WITH PASSWORD 'awesomegroup'
```

Grant privileges to the user cs516
```sh
ALTER USER cs516 WITH SUPERUSER
```

Now typing `\du` to terminate, you should see something like
```
                                   List of roles
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 cs516     | Superuser                                                  | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

Log back to your own user by `\q` and `exit`. You should see `your_name@your_machine` at the beginning of each line. 

Activate the virtualenv with 
```sh
source env/bin/activate
```
If it successes, a `(env)` will appear at the beginning of each line. 

Finally, 
```sh
flask run
```
Access the ip and the webpage should appear. 
