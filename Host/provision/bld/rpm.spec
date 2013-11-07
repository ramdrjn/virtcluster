#
#Commisioning scripts
#
Name: provision
Version: 1.0
Release: 1
License: license.txt
Summary: Common scripts and provisioning scripts
%description
Common scripts and provisioning scripts

#Ignore unlisted files so that they will not cause a build fail
%define _unpackaged_files_terminate_build 0
#Ignore auto dependency for python
%global __requires_exclude ^/usr/bin/python$

%package -n py-scripts-common
Summary: common python scripts
%description -n py-scripts-common
Common scripts

%install
%virtcluster_rm_br
%virtcluster_c_br_p
tar zxvf ./dist/py-scripts-common-1.0.linux-x86_64.tar.gz -C %{virtcluster_br}
tar zxvf ./dist/provisioning-1.0.linux-x86_64.tar.gz -C %{virtcluster_br}

%clean
%virtcluster_rm_br
rm -vrf ./dist

%files -n py-scripts-common -f ./bld/py-scripts-common.files
%virtcluster_host_scripts_perm

%files -f ./bld/provisioning.files
%virtcluster_host_scripts_perm
