Summary:	A daemon for the syslog system log interface
Name:		msyslog
Version:	1.08e
Release:	0.1
Group:		Daemons
License:	BSD
URL:		http://www.core-sdi.com/english/freesoft.html
Source0:	http://prdownloads.sourceforge.net/msyslog/%{name}-v%{version}-src.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR.patch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	syslog
Obsoletes:	syslog-ng
Provides:       syslogdaemon
Provides:	msyslog sysklogd

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

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/msyslog
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/msyslog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* AUTHORS ChangeLog INSTALL NEWS README
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/alat
%attr(755,root,root) %{_libdir}/alat/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
