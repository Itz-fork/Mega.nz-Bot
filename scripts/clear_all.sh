#!/usr/bin/bash

# Header
start() {
    echo -e "\e[1m\e[101m Script by Itz-fork \e[0m \n"
}

# Write down all sub dirs to one text file
write_sub_dirs() {
    find "$PWD" -type d | sort >> sub_dirs.txt
}

# Read sub_dirs.txt and delete __pycache__ folders
read_and_del() {
    no=0
    while read dir; do
    if [[ $dir == *"__pycache__"* ]]; then
        no=$((no + 1))
        rm -r "$dir" || Rmdir /S "$dir"
    fi
    done <sub_dirs.txt
    echo -e "\n🎉 \e[1mDone! Successfully removed $no directories \e[0m"
}

# Delete sub_dirs.txt file
del_txt_file() {
    rm -rf sub_dirs.txt || Del sub_dirs.txt
}

# Main function
main() {
    start
    write_sub_dirs
    read_and_del
    del_txt_file
}

main
