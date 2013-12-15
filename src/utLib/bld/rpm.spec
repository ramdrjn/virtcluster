#
#utLib rpm specification file
#
Name: utLib
Version: 1.0
Release: 1
Summary: utLib shared library
License: license.txt
AutoReq:no

%description
utLib shared library.

%install
%virtcluster_rm_br
%virtcluster_c_host_lib_p

cp ./lib/libutLib.so %{virtcluster_host_lib}

%clean
%virtcluster_rm_br

%pre
if [ "$1" = "1" ]; then
    #Install
    echo "%{_hostlibdir}" >>/etc/ld.so.conf
    /sbin/ldconfig
elif [ "$1" = "2" ]; then
    #Upgrade
    /sbin/ldconfig
fi

%files
%virtcluster_lib_perm
%{_hostlibdir}/libutLib.so
