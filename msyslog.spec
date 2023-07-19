Summary:	A daemon for the syslog system log interface
Summary(pl.UTF-8):	Modularny demon sysloga
Name:		msyslog
Version:	1.09d
Release:	1
Group:		Daemons
License:	BSD
Source0:	https://downloads.sourceforge.net/msyslog/%{name}-v%{version}-src.tar.gz
# Source0-md5:	641b4d01756b6aac5a5d332893aefce0
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	syslog.conf
Source4:	syslog.logrotate
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-pathes.patch
Patch2:		%{name}-configure.patch
Patch3:		%{name}-no-strip.patch
Patch4:		%{name}-link.patch
URL:		https://sourceforge.net/projects/msyslog/
BuildRequires:	autoconf
BuildRequires:	automake
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	syslogdaemon
Obsoletes:	sysklogd
Conflicts:	klogd
Conflicts:	syslog
Conflicts:	syslog-ng
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# uses symbols from binary
%define		skip_post_check_so	libmsyslog.so.*

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

%description -l pl.UTF-8
Projekt msyslog został przewidziany jako całkowicie nowa odmiana
projektu Bezpiecznego sysloga. Posiada całą jego funkcjonalność i
troszkę więcej. Niedopracowane rzeczy to support solarisa i
kompatybilność z Auditem. Cała wewnętrzna struktura jest przewidziana
do pracy z modułami wejścia i wyjścia, ustandaryzowanym międzymordziem
do łatwego rozwijania korzystając z specjalnych sterowników i
elastycznej konfiguracji. Aktualne moduły wyjściowe to: klasyczny,
mysql, peo, pgsql, regex i tcp. Dostępne moduły wejściowe to bsd,
linux, unix, tcp i udp.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

# missing "_" in filenames (but expected by makefiles)
%{__mv} src/modules/{im,im_}file.c
%{__mv} src/man/{im,im_}file.8

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-daemon-name=msyslogd

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/msyslog
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/msyslog
install -D %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/syslog.conf
install -D %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/syslog

install -d $RPM_BUILD_ROOT%{_mandir}/man{5,8}
cp -p src/man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p src/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add msyslog
%service msyslog restart

%preun
if [ "$1" = "0" ]; then
	%service msyslog stop
	/sbin/chkconfig --del msyslog
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS INSTALL NEWS README doc/* src/examples
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/msyslog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/syslog.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/syslog
%attr(754,root,root) /etc/rc.d/init.d/msyslog
%attr(755,root,root) %{_sbindir}/msyslogd
%attr(755,root,root) %{_sbindir}/peochk
%dir %{_libdir}/alat
%attr(755,root,root) %{_libdir}/alat/libmsyslog.so.%{version}
%{_mandir}/man5/syslog.conf.5*
%{_mandir}/man8/im_*.8*
%{_mandir}/man8/om_*.8*
%{_mandir}/man8/peochk.8*
%{_mandir}/man8/syslogd.8*
