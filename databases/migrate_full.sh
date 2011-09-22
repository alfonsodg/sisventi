#Modify -p(password) with the proper one to mysql
#mysqldump -u root -proot sisventi --no-create-info --complete-insert > sisventi.sql
mysqladmin -u root -proot drop sisventi
mysqladmin -u root -proot create sisventi
rm -f *table
read -p "Cree las tablas en web2py"
read -p "Listo?"
mysql sisventi -u root -proot < sisventi.sql
