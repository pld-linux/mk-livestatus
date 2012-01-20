Summary:	Accessing Nagios status data
#Summary(pl.UTF-8):
Name:		mk-livestatus
Version:	1.1.12
Release:	0.1
License:	unknown
Group:		Applications
Source0:	http://www.mathias-kettner.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	ddf1444874193316289d6c8cf71fa79d
URL:		http://mathias-kettner.de/checkmk_livestatus.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/unixcat
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.o
