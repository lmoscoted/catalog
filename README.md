# Item Catalog App

Item Catalog App is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system provided by third-party authentication & authorization service (Google). Registered users will have the ability to post, edit and delete their own items/categories. In the same way, by implementing a Local System Permission, an user can only edit or delete an item/category if it has been created by him. Moreover, this app has three JSON endpoints that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog. 




# What you need to have installed

This project makes use of a Linux-based virtual machine (VM).
You need to have installed:

* VirtualBox: For this project I used VirtualBox 5.1.38. This tool can be donwloaded [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.
* Vagrant: Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download the 2.2.0 version of this tool in this [link](https://www.vagrantup.com/).

You'll need to use a Unix-style terminal on your computer. If you are using a Mac or Linux system, your regular terminal program will do just fine. On Windows, we recommend using the Git Bash terminal that comes with the Git software. If you don't already have Git installed, download Git from [git-scm.com](https://git-scm.com/downloads).


## Download the VM configuration
You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Alternately if you are familiar with GitHub, you can use Github to fork and clone [this repository](https://github.com/udacity/fullstack-nanodegree-vm).


This will give you all packages  and support software needed for this project.

## Start the virtual machine
From your terminal, inside the vagrant subdirectory, which is located in  the either FSND-Virtual-Machine or fullstack-nanodegree-vm directory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!
If you want to exit from the Linux machine  run `Ctrl + D`

## Donwload the repository
After verifying that your Linux VM is working, now you need to download the project files. In order to do that, you can use GitHub to fork and clone [this repository](https://github.com/lmoscoted/catalog.git)

That repository must put inside the vagrant subdirectory.


# How to run it?
 
Firstly, you need to be logged on the linux session by running _vagrant up_ and _vagrant ssh_ inside the vagrant subdirectory on your terminal. Then, You need to change directory to the catalog subdirectory in your Linux VM. You can use either the DB file that I used for this project or you can create a new database with your own data. If you choose to create a new one, you need to edit only the rows from the csv files. Then, inside the catalog folder, you need to run `python database_setup.py`to create the database model for this project. Later, by running `python lotsofcatalogitems.py`, you will populate the database with all data. Finally, you need to run the next command:


```
python application.py
```

After that step, you will be able to access to the website project by typing on your web browser whether _localhost:5000/catalog_ or _localhost:5000_. 





