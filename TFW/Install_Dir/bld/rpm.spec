#
#Test binaries
#
Name: test_bin
Version: 1.0
Release: 1
Summary: Test binaries
License: license.txt

%description
Test Binaries

%install
%virtcluster_rm_br
%virtcluster_c_testbin_p

cp ./baseLib-FT.exe %{virtcluster_testbin}
cp ./baseLib-ST.exe %{virtcluster_testbin}
cp ./dsLib-FT.exe %{virtcluster_testbin}
cp ./dsLib-ST.exe %{virtcluster_testbin}
cp ./msgLib_Cli-ST.exe %{virtcluster_testbin}
cp ./msgLib_Srv-ST.exe %{virtcluster_testbin}

%clean
%virtcluster_rm_br

%files
%virtcluster_bin_perm
%{_testbindir}/baseLib-FT.exe
%{_testbindir}/baseLib-ST.exe
%{_testbindir}/dsLib-FT.exe
%{_testbindir}/dsLib-ST.exe
%{_testbindir}/msgLib_Cli-ST.exe
%{_testbindir}/msgLib_Srv-ST.exe
