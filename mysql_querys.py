QueryToCreateClients = "CREATE TABLE IF NOT EXISTS Clients(ID varchar(11),\
                        client_id int AUTO_INCREMENT PRIMARY KEY, UNIQUE KEY(ID),\
                        public_key VARCHAR(2000) NOT NULL,\
                        private_key VARCHAR(2000) NOT NULL);"
QueryToCreateTrasactions = "CREATE TABLE IF NOT EXISTS Transactions(transaction_id int AUTO_INCREMENT PRIMARY KEY NOT NULL,\
                            value int NOT NULL,client_id int NOT NULL,UNIQUE KEY(transaction_id),\
                            date datetime NOT NULL,hash VARCHAR(128) NOT NULL,\
                            FOREIGN KEY(client_id) REFERENCES Clients(client_id));"
QueryToUseDb = "USE bank_db"
QueryToDropTransactions = "DROP TABLES Transactions"
QueryToDropClients = "DROP TABLES Clients"
