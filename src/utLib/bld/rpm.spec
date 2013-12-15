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

%files
%virtcluster_lib_perm
%{_hostlibdir}/libutLib.so
