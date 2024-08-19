#!/bin/bash

function confirmacion() {
    read -r -p "WARNING: ¡LAUNCHING THIS ACTION WILL DELETE ALL THE INFORMATION ON THE DATABASE!. ¿ARE YOU SURE YOU WANT TO CONTINUE? [Y/n]" confirmacion
    confirmacion=${confirmacion,,}
    if [[ $confirmacion =~ ^(y|yes|Y|YES)$ ]]; then
        return 0
    else
        return 1
    fi
}

function mostrar_menu() {
    echo "Choose an option:"
    echo "1) Launch application"
    echo "2) Reset application (DANGER ZONE)"
    echo "0) Exit "
}

function attemp_install() {
    find .env;
    if [ $? -ne 0 ]; then
        echo "Config file not found. Proceeding to installation..."
        read -r -p "Enter the database ROOT password: " db_password
        while [ -z "$db_password" ]; do
            read -r -p "Password cannot be empty. Please enter the database password: " db_password
        done
        read -r -p "Enter the database name: " db_name
        while [ -z "$db_name" ]; do
            read -r -p "Database name cannot be empty. Please enter the database name: " db_name
        done
        read -r -p "Enter the database user: " db_user
        while [ -z "$db_user" ]; do
            read -r -p "Database user cannot be empty. Please enter the database user: " db_user
        done
        read -r -p "Enter the database user password: " db_user_password
        while [ -z "$db_user_password" ]; do
            read -r -p "Database user password cannot be empty. Please enter the database user password: " db_user_password
        done
        read -r -p "Enter the database host: " db_host
        while [ -z "$db_host" ]; do
            read -r -p "Database host cannot be empty. Please enter the database host: " db_host
        done
        read -r -p "Enter the Django secret key. It can be generated at https://djecrety.ir/ : " secret
        while [ -z "$secret" ]; do
            read -r -p "Secret key cannot be empty. Please enter the secret key: " secret
        done
        read -r -p "Enter the fortnite API secret key. It can be generated at https://dash.fortnite-api.com/account by logging in via Discord and following the instructions: " fort_secret
        while [ -z "$fort_secret" ]; do
            read -r -p "Fortnite API cannot be empty. Please enter the Fortnite API secret key: " fort_secret
        done
        read -r -p "Will the server run in production mode? [Y/n]" production
        if [[ $production =~ ^(y|yes|Y|YES)$ ]]; then
            echo "Production mode enabled. Please remember to set up the allowed hosts in the settings.py file."
            production="True"
        else
            echo "Production mode disabled. Do not deploy this server on production."
            production="False"
        fi
        read -r -p "Enter the server port: " port
        while [ -z "$port" ]; do
            read -r -p "Server port cannot be empty. Please enter the server port: " port
        done
        echo "Creating config file..."
        echo "MYSQL_ROOT_PASSWORD=$db_password
MYSQL_DATABASE=$db_name
MYSQL_USER=$db_user
MYSQL_PASSWORD=$db_user_password
MYSQL_HOST=$db_host
DJANGO_SECRET_KEY=$secret
FORT_SECRET=$fort_secret
DJANGO_DEBUG=$production
PORT=$port" >.env
    else
        echo "Config file found."
    fi
}

while true; do
    attemp_install
    mostrar_menu
    read -r -p "Type your option [0-2]: " option

    case $option in
        1)
            echo "Launching application, please wait..."
            cp .env SkinList/.env
            docker-compose up --build
            break
            ;;
        2)
            if confirmacion; then
                echo "Resetting application..."
                #rm .env;
                #Detiene los contenedores en caso de que esten en ejecucion
                docker stop skinlist-app-1;
                docker stop skinlist-db-1;
                #Elimina los contenedores
                docker rm skinlist-app-1;
                docker rm skinlist-db-1;
                #Elimina la imagen del API y las que no están en uso, no hace falta borrar la SQL
                docker rmi skinlist-app;
                docker image prune;
                #Elimina los volúmenes de la base de datos (API no usa volúmenes)
                docker volume rm skinlist_mysql_data;
            else
                echo "Operation cancelled."
            fi
            ;;
        0)
            echo "Closing script."
            exit 0
            ;;
        *)
            echo "Not valid input."
            ;;
    esac
done