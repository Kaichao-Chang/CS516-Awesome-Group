mypath=`realpath $0`
mybase=`dirname $mypath`
cd $mybase

sudo -u postgres bash setup.sh