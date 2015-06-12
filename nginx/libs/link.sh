#!/bin/bash
# 做软链.


# 参数判断.
if [ "$#" != "6" ]
then
    echo "Parameter num must be 4" 1>&2
fi


# 变量列表.
nginx_dir=$1
product=$2
_type=$3
idc=$4
nginx_ssl_origin_dir=$5
nginx_ssl_dest_dir=$6


# 进入目录.
cd $nginx_dir ||exit 1


# 拷贝 ssl 证书.
if ! test -d $nginx_ssl_dest_dir
then
    mkdir $nginx_ssl_dest_dir
fi
/bin/cp -f $nginx_ssl_origin_dir/* $nginx_ssl_dest_dir/ 1>&2 ||exit 1


# 进入 sites-enabled.
if ! test -d sites-enabled
then
    mkdir sites-enabled ||exit 1
fi
cd sites-enabled ||exit 1


# 如果不是目录, 退出.
if ! test -d ../sites-available/$product/${_type}/$idc/
then
    echo "../sites-available/$product/${_type}/$idc/ is not a directory." 1>&2
    exit 1
fi


# 如果目录为空, 退出.
files=`ls ../sites-available/$product/${_type}/$idc/`
if [ "$files" == "" ]
then
    echo "../sites-available/$product/${_type}/$idc/ not include any files." 1>&2
    exit 1
fi


# 做软链.
for file in $files
do
    if ! ln -sf ../sites-available/$product/${_type}/$idc/$file $file
    then
        echo "exec ln -sf ../sites-available/$product/${_type}/$idc/$file $file failed." 1>&2
        exit 1
    fi
done


# 除了做域名的软链之外, 还要做日志格式的软链.
if ! test -d ../log_format-enabled/
then
    mkdir ../log_format-enabled/ ||exit 1
fi
cd ../log_format-enabled/ ||exit 1
if test -d ../log_format-available/$product/${_type}/$idc/
then
    files=`ls ../log_format-available/$product/${_type}/$idc/`
    for file in $files
    do
        if ! ln -sf ../log_format-available/$product/${_type}/$idc/$file $file
        then
            echo "exec ln -sf ../log_format-available/$product/${_type}/$idc/$file $file failed." 1>&2
            exit 1
        fi
    done
fi


exit 0
