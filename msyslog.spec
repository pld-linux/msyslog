Summary:	A daemon for the syslog system log interface
Summary(pl):	Modularny demon sysloga
Name:		msyslog
Version:	1.09c
Release:	1
Group:		Daemons
License:	BSD
Source0:	http://dl.sourceforge.net/msyslog/%{name}-v%{version}-src.tar.gz
# Source0-md5:	1e9119a051f3febf79802bb059a2f727
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	syslog.conf
Source4:	syslog.logrotate
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-pathes.patch
URL:		http://www.core-sdi.com/english/freesoft.html
BuildRequires:	autoconf
BuildRequires:	automake
Requires(post,preun):	/sbin/chkconfig
Provides:	syslogdaemon
Obsoletes:	syslog
Obsoletes:	sysklogd
Obsoletes:	klogd
Obsoletes:	syslog-ng
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is intended as a whole revision of previous Secure
Syslogd project (wich is unsupported by now). It has all
functionalities and some more. The remaining things are Solaris
support and Audit compatibility (on the works). The whole internal
structure was redesigned to work with input and output modules,
standardizing interfaces to facilitate development for using special
devices and flexible configurations. Current available output modules
are classic, mysql, peo, pgsql, regex and tcp. Available input modules
are bsd, linux, unix, tcp and udp.

%description -l pl
Projest msyslog zosta³ przewidzany jako ca³kowicie nowa odmiana
projektu Bezpiecznego sysloga. Posiada ca³± jego funkcjonalno¶æ i
troszke wiêcej. Niedopracowane rzeczy to support solarisa i
kompatybilno¶æ z Auditem. Ca³a wewnêtrzna struktura jest przewidziana
do pracy z modu³ami wejscia i wyj¶cia, ustandaryzowanym miêdzymordziem
do ³atwego rozwijania korzystaj±c z specjalnych sterowników i
elastycznej konfiguracji. Aktualne modu³y wyj¶ciowe to: klasyczny,
mysql, peo, pgsql, regex i tcp. Dostêpne modu³y wej¶ciowe to bsd,
linux, unix, tcp i udp.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1
%patch1 -p0

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%configure \
	--with-daemon-name=msyslogd

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/msyslog
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/msyslog
install -D %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/syslog.conf
install -D %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/syslog

install -d $RPM_BUILD_ROOT%{_mandir}/man{5,8}
install src/man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install src/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add msyslog
if [ -f /var/lock/subsys/msyslog ]; then
        /etc/rc.d/init.d/msyslog restart >/dev/null 2>&1
else
        echo "Run \"/etc/rc.d/init.d/msyslog start\" to start msyslog
daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/msyslog ]; then
                /etc/rc.d/init.d/msyslog stop >&2
        fi
        /sbin/chkconfig --del msyslog
fi

%files
%defattr(644,root,root,755)
%doc doc/* AUTHORS INSTALL NEWS README src/examples
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/*.conf
%attr(640,root,root) /etc/logrotate.d/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/alat
%attr(755,root,root) %{_libdir}/alat/*
%{_mandir}/man?/*
