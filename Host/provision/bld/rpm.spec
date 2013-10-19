#
#Commisioning scripts
#
Name: provision
Version: 1.0
Release: 1
Summary: Commisioning scripts
License: license.txt

%description
Commisioning scripts

%install
%virtcluster_rm_br
%virtcluster_host_p
%virtcluster_host_provision_p

cp ./src/common.py %{virtcluster_host_provision_dir}
cp ./src/cli_mon.py %{virtcluster_host_provision_dir}
cp ./src/py_libvirt.py %{virtcluster_host_provision_dir}

%clean
%virtcluster_rm_br

%files
%virtcluster_host_scripts_perm
%{_hostprovisiondir}/common.py
%{_hostprovisiondir}/cli_mon.py
%{_hostprovisiondir}/py_libvirt.py
