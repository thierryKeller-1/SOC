#!/bin/bash  

project_dir="/home/keller/Documents/Jobdev/G2A/SOC" 
python_file="$project_dir/__main__.py"  
log_file="$project_dir/logfile.log"

# Vérifier si le fichier Python existe  
if [[ -f "$python_file" ]]; then  
    echo "Lancement de $python_file..."
    source "$project_dir/venv/bin/activate"
    echo "$(date '+%Y-%m-%d %H:%M:%S') : process start" | tee -a "$log_file"  
    python3 "$python_file" >> "$log_file" 2>&1 
    deactivate
    echo "$(date '+%Y-%m-%d %H:%M:%S') : process finished." | tee -a "$log_file" 
else  
    echo "Erreur : $python_file n'existe pas."  
fi  

# */3 * * * * DISPLAY=:0 /home/keller/Documents/Jobdev/G2A/SOC/setup.sh