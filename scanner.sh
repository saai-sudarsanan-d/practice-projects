#! /usr/bin/bash

# Configure Output file Setting
OUT_DIR=$(pwd)
if [ -z "$1" ];
then
	sleep 0
else
	OUT_DIR=$1
fi

# Detect Directory - Create it if not already created
IFS=$'\n'
FNAME="$(date +"%d%m%y-%H%M%S").rk"
if [ -d $OUT_DIR ];
then
    echo "Logging to $OUT_DIR"
    touch $OUT_DIR/$FNAME
else
    echo "The directory doesn't exist, please provide absolute path."
    exit	
fi

# Function to Iterate through the directories recursively
function iter_dir(){
    for OBJ in $(ls $1);
    do
        if [ -d $1/$OBJ ];
        then
            iter_dir $1/$OBJ
        else
            echo $(md5sum $1/$OBJ) >> $OUT_DIR/$FNAME
        fi
    done
}

# Start Scan
echo "Starting Scan, this may take a while, so please feel free to do something else in the mean time."

# Find out what directories to scan
ALL=false
FILES_TO_SCAN=()

for DIR in $(cat $(pwd)/scanme);
do
    if [ "$DIR" = "all" ];
    then
        echo "You have chosen to scan all directories. This is recommended, but takes time."
        ALL=true
    else
        DIRS_TO_SCAN+=( $DIR )
    fi
done

if [ "$ALL" = "true" ];
then
    echo "Sorry, this feature has not been implemented yet."
fi

# Send each directory to the iter function
for DIR in ${DIRS_TO_SCAN[@]};
do
    iter_dir $DIR
done
