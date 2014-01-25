#
#cpackgen_kmod rpm specification file
#
Name: cpackgen_kmod
Version: 1.0
Release: 1
Summary: cpackgen generator and receiver kernel module
License: license.txt
AutoReq:no

%description
cpackgen packet generator and receiver kernel module code.

%install
%virtcluster_rm_br
%virtcluster_c_br_p

cp -r ./obj/lib %{virtcluster_br}

%clean
%virtcluster_rm_br

%files
%virtcluster_kmod_perm
/lib
