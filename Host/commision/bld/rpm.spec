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
%virtcluster_host_scripts_p
%define virtcluster_commision_dir %{virtcluster_host_scripts}/commision/
mkdir -p %{virtcluster_commision_dir}

cp ./src/common.py %{virtcluster_commision_dir}
cp ./src/cli_mon.py %{virtcluster_commision_dir}
cp ./src/py_libvirt.py %{virtcluster_commision_dir}

%clean
%virtcluster_rm_br

%files
%virtcluster_host_scripts_perm
%{_hostscriptsdir}/commision/common.py
%{_hostscriptsdir}/commision/cli_mon.py
%{_hostscriptsdir}/commision/py_libvirt.py
