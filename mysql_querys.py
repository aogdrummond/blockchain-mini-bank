QueryToCreateClients = "CREATE TABLE IF NOT EXISTS Clients(CPF varchar(11),\
                        client_id int AUTO_INCREMENT PRIMARY KEY, UNIQUE KEY(CPF));"
QueryToCreateTrasactions = "CREATE TABLE IF NOT EXISTS Transactions(value int NOT NULL,\
                            date datetime NOT NULL,transaction_id int AUTO_INCREMENT PRIMARY KEY NOT NULL,\
                            client_id int NOT NULL,UNIQUE KEY(transaction_id),\
                            FOREIGN KEY(client_id) REFERENCES Clients(client_id));"
QueryToUseDb = "USE bank_db"
QueryToDropTransactions = "DROP TABLES Transactions"
QueryToDropClients = "DROP TABLES Clients"
