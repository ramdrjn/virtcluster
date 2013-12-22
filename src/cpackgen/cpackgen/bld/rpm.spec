#
#cpackgen rpm specification file
#
Name: cpackgen
Version: 1.0
Release: 1
Summary: cpackgen generator and receiver
License: license.txt
AutoReq:no

%description
cpackgen packet generator and receiver code.

%install
%virtcluster_rm_br
%define cpackgen_dir %{virtcluster_host_dir}/cpackgen
mkdir -p %{cpackgen_dir}

cp ./bin/cpackgen.exe %{cpackgen_dir}

%clean
%virtcluster_rm_br

%files
%virtcluster_bin_perm
%{_hostdir}/cpackgen/cpackgen.exe
