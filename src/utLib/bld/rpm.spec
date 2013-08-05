#
#utLib rpm specification file
#
Name: utLib
Version: 1.0
Release: 1
Summary: utLib shared library
License: license.txt

%description
utLib shared library.

%install
%virtcluster_rm_br
%virtcluster_c_lib_p

cp ./lib/libutLib.so %{virtcluster_lib}

%clean
%virtcluster_rm_br

%files
%virtcluster_lib_perm
%{_libdir}/libutLib.so
