# SkinList

This application provides a list of all the cosmetics available on Fortnite, and the ability to save certain cosmetics on a wishlist, sending alerts to the users whenever an item from their wishlist becomes available at the game shop.

## How to deploy

### System Requirements
- Docker
- At least 4GB of RAM

### Installation

1. Pull the repository
```bash
git pull https://github.com/CDisidoro/SkinList.git
```
2. Run the run.sh script
```bash
./run.sh
```
3. A installation assistant will be shown. Follow the steps on the assistant, typing all of the requested information.
```
Config file not found. Proceeding to installation...
Enter the database ROOT password:
Enter the database name:
Enter the database user:
Enter the database user password:
Enter the database host:
Enter the Django secret key. It can be generated at https://djecrety.ir/ :
Enter the fortnite API secret key. It can be generated at https://dash.fortnite-api.com/account by logging in via Discord and following the instructions:
Will the server run in production mode? [Y/n]
Enter the server port:
```
4. Once the installation assistant finishes, a menu will be shown. Type the option 1 to launch the application.
```
Choose an option:
1) Launch application
2) Reset application (DANGER ZONE)
3) Exit
```
1. Once the application launches, go to (http://localhost:< The port you put on the configuration file>)