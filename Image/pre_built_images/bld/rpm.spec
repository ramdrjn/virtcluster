#
#Image rpm
#
Name: virtcluster-image
Version: 1.0
Release: 1
Summary: Virtcluster boot images
License: license.txt

%description
Virtcluster boot and os images

%install
%virtcluster_rm_br
%virtcluster_host_p
%virtcluster_host_commision_p
%define virtcluster_image_dir %{virtcluster_host_commision_dir}/images/
mkdir -p %{virtcluster_image_dir}

cp ./images/manifest %{virtcluster_image_dir}
cp ./images/virtcluster-image-*.tgz %{virtcluster_image_dir}

%clean
%virtcluster_rm_br

%files
%virtcluster_host_scripts_perm
%{_hostcommisiondir}/images/manifest
%{_hostcommisiondir}/images/virtcluster-image-*.tgz

