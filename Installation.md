## Install instructions 
### Using setup script
1. Clone this repository by using this command on terminal

```
git clone https://github.com/Nantawat6510545543/ku-polls.git
```

2. Change directory to project directory

```
cd ku-polls
```

3. Execute the setup script

    for **Mac/Linux** use this command: 
    ```
    chmod +x linux-setup-script.sh
    ./setup-linux.sh
    ```
   
    for **Windows** use this command:
    ```
    window-setup-script.bat
    ```
Note: You may continue follow manual installation no.8 to see a sample graph

### Manual Installation
1. Clone this repository by using this command on terminal

```
git clone https://github.com/Nantawat6510545543/ku-polls.git
```

2. Change directory to project directory

```
cd ku-polls
```

3. Create and activate a virtual environment

    for **Mac/Linux** use this command: 
    ```
    python -m venv env           # create the virtual env in "env/", only 1 time
    . env/bin/activate           # start the virtual env in bash or zsh
    ```
   
    for **Windows** use this command:
    ```
    python -m venv env
    . .\env\Scripts\activate
    ```

4. Create a .env file by copying the contents of sample.env
   
    for **Mac/Linux** use this command:
    ```
   cp sample.env .env
   ```
    
   for **Windows** use this command:
    ```
   copy sample.env .env
   ```
   
5. Install dependencies by following command

```
pip install -r requirements.txt
```

6. Create a new database by running migrations

```
python manage.py migrate
```

7. Then import data using “loaddata”

```
python manage.py loaddata data/polls.json data/users.json
```

8. (optional) Load vote data to see a sample graph
```
python manage.py loaddata data/vote.json
```