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

while true; do
    mostrar_menu
    read -r -p "Type your option [0-2]: " option

    case $option in
        1)
            echo "Launching application, please wait..."
            docker-compose up --build
            break
            ;;
        2)
            if confirmacion; then
                echo "Resetting application..."
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