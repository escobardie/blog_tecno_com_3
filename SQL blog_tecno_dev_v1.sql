drop database blog_tecno_dev_v1;

show databases;
CREATE DATABASE blog_tecno_dev_v1;
USE blog_tecno_dev_v1;
SHOW TABLES;


/* DDL CON ENFOQUE EN SEGURIDAD*/
/* creamos un usuario con persimos solo para acceder a la base de datos db_blog*/
/* usuario: user1,  password: user-1 */
CREATE USER 'user1'@'localhost' identified by 'user-1';

GRANT ALL PRIVILEGES ON blog_tecno_dev_v1.* TO user1@localhost;
FLUSH PRIVILEGES;

DROP USER 'user1'@'localhost';

/* DDL CON ENFOQUE EN SEGURIDAD*/


SHOW TABLES;