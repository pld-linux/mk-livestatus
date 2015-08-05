Summary:	Accessing Nagios status data
Name:		mk-livestatus
Version:	1.2.6p9
Release:	1
License:	GPL v2
Group:		Applications
# Source0Download: https://mathias-kettner.de/check_mk_download_source.html
Source0:	https://mathias-kettner.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	a01b3cc372f5dbe672eee29afeb94dd5
Patch0:		socket-path.patch
URL:		http://mathias-kettner.de/checkmk_livestatus.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	nagios >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios
%define		_libdir		%{_prefix}/%{_lib}/nagios

%description
Livestatus. Just as NDO, Livestatus make use of the Nagios Event
Broker API and loads a binary module into your Nagios process. But
other then NDO, Livestatus does not actively write out data. Instead,
it opens a socket by which data can be retrieved on demand.

The socket allows you to send a request for hosts, services or other
pieces of data and get an immediate answer. The data is directly read
from Nagios' internal data structures. Livestatus does not create its
own copy of that data. Beginning from version 1.1.2 you are also be
able retrieve historic data from the Nagios log files via Livestatus.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-nagios4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} -j1 install \
	pkglibdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

# sample line that should be added to nagios.cfg for this module to work
install -d $RPM_BUILD_ROOT%{_sysconfdir}
echo 'broker_module=%{_libdir}/livestatus.o' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/livestatus-load.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q nagios restart

%postun
if [ "$1" = 0 ]; then
	%service -q nagios restart
fi


%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/livestatus-load.cfg
%attr(755,root,root) %{_bindir}/unixcat
%attr(755,root,root) %{_libdir}/livestatus.o
