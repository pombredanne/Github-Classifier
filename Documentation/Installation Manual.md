# Installation Manual

## Requirements

* [Python 2.7 64bit](https://www.python.org/downloads/release/python-2713/)
* [pip (module manager)](https://packaging.python.org/installing/#install-pip-setuptools-and-wheel)
* [Firefox 50](https://www.mozilla.org/en-US/firefox/new/)
* Screen size >= (1280px x 600px)
* RAM > 4GB

## Notes

This guide can be followed to get the frontend running on your local system. If you don't want to install one of the listed dependencies or want to emulate a preconfigured client image, please refer to the section `VirtualBox`. Even though running the client in an emulation should only be considered in exceptional cases.

Please make sure that the working / installation **directory** of Python and the g++ compiler do **not contain special characters** such as German umlauts.
Keep in mind that installations with pip require **super user rights**.

## Modules

_Either downloaded and installed with the command `pip install path/to/file.whl` (on Windows) or installed with `pip install xxx` (on UNIX or OS x)._ 

1. [numpy + mkl](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
2. [scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)
3. [cherrypy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#cherrypy) on Windows **or** `paste` on UNIX or OS x for compatibility reasons

_Installed with the command `pip install xxx`_

1. bottle
2. keras
3. sklearn
4. nltk
5. gensim
6. pattern
7. theano
8. demjson

## Other

* [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
* [A 64bit g++ compiler](http://deeplearning.net/software/theano/install_windows.html#gcc)
* Keras has to be configured to use Theano (instead of Tensorflow). In UNIX systems, this can be changed at `~/.keras/keras.json`. The same file can be found at `%userprofile/.keras/keras.json` on Windows.

## When everything is said and done

Now that every library and dependency is installed, you can open the **command shell** as a superuser in the folder `Application`. Type `python start.py` and wait until the GUI is being opened in a new Tab in Firefox (this will take a couple of minutes). Meanwhile, you can learn how to interact with the GUI in the separate documentation file `Frontend Manual.md`. Note that you can read the docfiles in the User Interface as well.

If you want to test a file  of repository links without a GUI (e.g. the Appendix B file) switch into the folder `Application` and place your input file. It must consist of a line separated list of GitHub repository URLs. Open the command shell and type `python predict.py <yourfile>` and wait until the script has finished. The results will be saved at `classification_result.txt` in the same directory. 

_Note: If there are still packages missing that do not show up in the list, please install them via pip._


## VirtualBox

Instead of installing everything from above, you can also use the VM image. A virtualisation software such as Oracle VirtualBox is needed in this case as well as a unzipping tool such as 7zip. Please be sure to reserve enough RAM for the emulation.

 > [Download VM](https://drive.google.com/open?id=0B3nBoE608aQyT0F2bWh1SDdXSTQ)

Root login credentials are
```
Username: informaticup
Password: informaticup
```

Once Ubuntu has booted, change to the folder `~/GithubClassifier/` and replace it with the folder `GithubClassifier` of our submission. Open the folder and run `python Application/start.py` inside the terminal as root.

Note that [our project repository](https://github.com/Ichaelus/Github-Classifier) is now public and visible for everyone.

## And what about the Backend?

We had many thoughts about running the backend locally as well or not. This would imply running two localhosts (Apache with PHP and Bottle with Python) synchronously as well as a local MySQL database - all that leads to many irrelevant and _OS-restricted_ dependencies.

Therefore we decided to rely on the remote server even in the final submission, while providing you both the source code running on the machine (located in the submission folder `/Backend/`) and full access to the server and its database.

```
Accessible via PuTTY on SSH port 7822
IP:  67.209.116.156
Username: <provided separately>
Password: <provided separately>
Backend location: /var/www/html
Database access: http://67.209.116.156/phpmyadmin/
Database username: <provided separately>
Database password: <provided separately>
```

If you still insist running the Backend locally, follow this guideline:

* Run **A**pache, **M**ySQL and **P**HP on your local machine. Note that the port of this localhost must be set different to 8080
* Installing PHPMyAdmin as well will make it easier to import database files
* Make sure Apache's DocumentRoot is set to the /Backend folder of our submission. Give the User/Group which runs apache access right to the same folder.
* Create a new MySQL user and import the database files located in /Database/SQL dumps/u51019db1.sql into a previously created database called `u51019db1`.
* Now switch to /Backend/mysqli_class.php and update username, password, server name and database name
* Go to http://localhost:<port> to see if everything is running
* The last step is to replace every occurrence of `67.209.116.156` to `localhost:<port>`. This should be limited to the files:
    * /Application/Models/DatabaseCommunication.py
    * /Application/Views/scripts/crawler_local.js
* Restart the application and enjoy :-)
