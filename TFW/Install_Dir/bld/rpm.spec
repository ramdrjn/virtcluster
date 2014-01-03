#
#Test binaries
#
Name: test_bin
Version: 1.0
Release: 1
Summary: Test binaries
License: license.txt
AutoReq:no

%description
Test Binaries

%install
%virtcluster_rm_br
%virtcluster_c_host_testbin_p

cp ./baseLib-FT.exe %{virtcluster_host_testbin}
cp ./baseLib-ST.exe %{virtcluster_host_testbin}
cp ./dsLib-FT.exe %{virtcluster_host_testbin}
cp ./dsLib-ST.exe %{virtcluster_host_testbin}
cp ./msgLib_Cli-ST.exe %{virtcluster_host_testbin}
cp ./msgLib_Srv-ST.exe %{virtcluster_host_testbin}
cp ./utLib-IT.exe %{virtcluster_host_testbin}

%clean
%virtcluster_rm_br

%files
%virtcluster_bin_perm
%{_hosttestbindir}/baseLib-FT.exe
%{_hosttestbindir}/baseLib-ST.exe
%{_hosttestbindir}/dsLib-FT.exe
%{_hosttestbindir}/dsLib-ST.exe
%{_hosttestbindir}/msgLib_Cli-ST.exe
%{_hosttestbindir}/msgLib_Srv-ST.exe
%{_hosttestbindir}/utLib-IT.exe
