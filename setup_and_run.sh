#!/bin/bash

# Fonction pour vérifier et installer une librairie Python
function install_if_not_installed() {
    local module_name=$1
    local package_name=$2

    python -c "import $module_name" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Installation de $package_name..."
        pip install $package_name
    else
        echo "$module_name est déjà installé."
    fi
}

# Vérification des librairies nécessaires
install_if_not_installed "PIL" "pillow"  # Pillow est importé sous le nom "PIL"
install_if_not_installed "tkinter" "tkinter"

# Lancer le code principal
echo "Lancement du code principal..."
python src/main.py  # Remplacez "main.py" par le nom de votre fichier Python principal