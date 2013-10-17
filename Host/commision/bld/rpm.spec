#
#Commisioning scripts
#
Name: commision
Version: 1.0
Release: 1
Summary: Commisioning scripts
License: license.txt

%description
Commisioning scripts

%install
%virtcluster_rm_br
%virtcluster_host_p
%virtcluster_host_commision_p

cp ./src/common.py %{virtcluster_host_commision_dir}
cp ./src/cli_mon.py %{virtcluster_host_commision_dir}
cp ./src/py_libvirt.py %{virtcluster_host_commision_dir}

%clean
%virtcluster_rm_br

%files
%virtcluster_host_scripts_perm
%{_hostcommisiondir}/common.py
%{_hostcommisiondir}/cli_mon.py
%{_hostcommisiondir}/py_libvirt.py
