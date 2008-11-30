Summary:	Client to configure an IPv6 tunnel to Hexago's migration broker
#Summary(pl.UTF-8):	-
Name:		tspc
Version:	2.1.1
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/t/tspc/%{name}_%{version}.orig.tar.gz
# Source0-md5:	-
Source1:	%{name}.init
Patch0:		%{name}-PLD.patch
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Connecting to the IPv6 Internet requires either a native connection
or the cooperation of a friendly server to provide you with a tunnel.

Tunnel Server Protocol Client (tspc), is a daemon to automate the
setup and maintenance of an IPv6 tunnel. This client will connect to
any migration broker which uses Hexago's implementation.

# %description -l pl.UTF-8
#TODO

%prep
%setup -q -n tspc2
%patch0 -p1

%build
%{__make} all \
	target=linux \
	CFLAGS="%{rpmcflags} -I../../include -I../../platform/linux" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir},/etc/sysconfig}

%{__make} install \
	target=linux \
	configdir=%{_sysconfdir}/tsp \
	install_bin=$RPM_BUILD_ROOT%{_sbindir} \
	installdir=$RPM_BUILD_ROOT%{_prefix}

mv $RPM_BUILD_ROOT%{_prefix}/template $RPM_BUILD_ROOT%{_sysconfdir}/tsp
mv $RPM_BUILD_ROOT%{_sbindir}/*.conf  $RPM_BUILD_ROOT%{_sysconfdir}/tsp
mv $RPM_BUILD_ROOT%{_prefix}/man/*    $RPM_BUILD_ROOT%{_mandir}

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
touch $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/tsp
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tsp/*.sh
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tsp/*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man?/*
