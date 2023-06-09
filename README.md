# Blockchain Mini Bank

### This software was developed as a practice to integrate different skills aiming to design an ATM's software, responsible for identifying the user and applying the right operations to withdrawn money, deposit money and manages the account. It was then increased to allow real-time consultation of currency exchange rates and application of blockchain algorithms to ensure data consistency.

## **Installation**

#### Ps: although it is already tested and validated on Linux system, it still does not run smoothly on Windows.
### Make sure you have docker, docker-composed and git installed on your machine by typing in your command prompt: 

&nbsp;
```
python3 --version
docker -v
docker-compose -v
git --version
pip --version
```

### It should provide the installed versions. If any of them is not available to the system yet, install it beforehand.



&nbsp;

### Clone the repository with source code.

```
git clone https://github.com/aogdrummond/blockchain-mini-bank.git
```
&nbsp;

### Change working directory to app's.

```
cd blockchain_mini_bank
```

&nbsp;
### Create virtual environment.
```
python3 -m venv blockchain_bank_venv
```
&nbsp;


### Activate the virtual environment.

```
. blockchain_bank_venv\Scrips\activate [Windows] 
or
. blockchain_bank_venv\bin\activate [Linux/Mac] 
```
&nbsp;
### Install virtual environment dependencies.
```
pip install -r requirements.txt
```
&nbsp;

### Only in the case you are interest on persisting database's data when its container stops, inserts the field "volumes" like in the example below, in the following order:

```
 volumes:
     - path\to\storage\folder:/var/lib/mysql 
```
### The folder to storage must be empty.

&nbsp;

![Procedure to insert persistance](img/volume_change.png)

### If you aren't interested on persistance, the file may remain unchanged

&nbsp;
### Download image and run container for containerized dB.
```
docker-compose up
```
Tip: To acess the images available on DockerHub you need to be logged in to Docker. The quickest way on Windows is by installing Docker Desktop.

&nbsp;
### After those steps, the container with the database should be running and connected to your system, and the aplication is ready to run.


&nbsp;


## **How to use**


* ### If you are interested on using Flask functionality, to get currency exchange rates start running flask_app/view.py application. Otherwise you may skip this phase.

* ### Activate the API through the following command (remember, it must be inside the virtual environment!):
```
python3 flask_app/view.py
```
![Example of usage](img/running_flask.png)

&nbsp;

* ### Paste API's IP and port into .env file to adjust the environment variables

![Example of usage](img/env_variables.png)


* ### To start the application on your console, just run "main.py" file:

```
python3 main.py
```

* ### To use it just follow the commands in the console, like in the example below: 

&nbsp;


![Example of usage](img/usage_flow.png)


## **How to use the automatted tests**

### Unit tests:.

```
pytest tests\unit_tests.py 
```
### Integration tests:.

```
pytest tests\int_tests.py 
```

* **Be aware, the automatted tests clean the whole database after execution.**

### Updates on version 2.0

1 - Blockchain encryption for consistency

![Example of usage](img/database_hashes.png)

* The unique hashes allow the blockchain to be promptly reassembled to ensure all the transactions are valid. If one of the transactions is changed direcly in the database, the hash created with differ from expected, warning an inconsistency message.

2 - Real time exchange rate for various currencies:

![Example of usage](img/currency_rate.png)