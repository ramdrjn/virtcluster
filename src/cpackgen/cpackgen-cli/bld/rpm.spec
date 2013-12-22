#
#Cpackgen cli scripts
#
Name: cpackgen-cli
Version: 1.0
Release: 1
License: license.txt
Summary: CLI scripts for cpackgen
AutoReq:no
%description
cpackgen cli

#Ignore unlisted files so that they will not cause a build fail
%define _unpackaged_files_terminate_build 0
#Ignore auto dependency for python
#%global __requires_exclude ^/usr/bin/python$

%install
%virtcluster_rm_br
%virtcluster_c_br_p
tar zxvf ./dist/cpackgen-cli-*.tar.gz -C %{virtcluster_br}

%clean
%virtcluster_rm_br
rm -vrf ./dist

%files -f ./bld/cpackgen-cli.files
%virtcluster_scripts_perm
