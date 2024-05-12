printf '\e[8;32;114t' // Set window size to 32x114
printf '\033[40m' // Set background colour to black
printf '\033[33m' // Set forground colour to yellow/orange-ish
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
clear
python3 $SCRIPT_DIR/stillAlive.py