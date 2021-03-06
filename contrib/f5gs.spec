# Wben building an rpm from random git revision create a tag
# something like:
#
#	git tag -a v0.2
#
# followed by
#
#	./bootstrap && ./configure && make dist
#
# You may need to compile upstream versions of autoconf & automake.
# If so the RHEL I used gave build problems, when new versions were
# available in /usr/local/bin/ and in my PATH, which I overcame by
#
# rpmbuild --nodeps -ba contrib/f5gs.spec

Name:		f5gs
Version:	0.2
Release:	1
Summary:	F5 Graceful Scaling helper daemon
Group:		System Environment/Daemons
License:	BSD
URL:		https://github.com/kerolasa/f5gs
Source0:	%{name}-%{version}.tar.xz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: texinfo
BuildRequires: xz
BuildRequires: autoconf >= 2.69
BuildRequires: automake
Requires(post): chkconfig
Requires(postun): initscripts
Requires(preun): chkconfig
Requires(preun): initscripts

# Define init script directory.  %{_initddir} is available from RHEL 6
# forward; RHEL 5 knows only %{_initrddir}.
%{!?_initddir: %{expand: %%global _initddir %{_initrddir}}}

%description
This is a simple tcp daemon, which is intented to be used as a messanger
from a server to a F5 load balancing switch.  One is expected to make a
F5 switch to poll with a health check the f5gs daemon, that will tell the
state of the service.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
[ "%{buildroot}" != / ] && %{__rm} -rf "%{buildroot}"
%{__make} install DESTDIR=%{buildroot}
%{__install} -p -D -m 755 contrib/init.redhat %{buildroot}%{_initddir}/%{name}

%post
# Organizations that have working orchestration should remove post
# installation, upgrade, and service status actions.
if [ $1 -eq 1 ] ; then
	# Install
	/sbin/chkconfig --add %{name} || :
	/sbin/service %{name} start >/dev/null 2>&1 || :
else
	# Upgrade
	/sbin/service %{name} restart >/dev/null 2>&1 || :
fi
if [ "$(%{name})" = 'current status is: unknown' ]; then
	%{name} -e >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
	# Uninstall
	/sbin/service %{name} stop >/dev/null 2>&1 || :
	/sbin/chkconfig --del %{name} || :
	# Some want to remove state files automatically.  Unfortunately
	# there is no %{__runstatedir} so this is as good one can get
	# the removal.
	# %{__rm} -rf %{_localstatedir}/run/%{name}
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%doc %_mandir/man*/*
%_bindir/*
%{_initddir}/%{name}
%_datadir/%{name}/*

%changelog
* Thu Dec 12 2013  Sami Kerola <kerolasa@iki.fi>
- Fix installation and upgrade time actions.

* Tue Oct 22 2013  Sami Kerola <kerolasa@iki.fi>
- Add pre-script example to rpm.

* Tue Oct 15 2013  Sami Kerola <kerolasa@iki.fi>
- Add init script.

* Mon Oct 14 2013  Sami Kerola <kerolasa@iki.fi>
- Add a rpm spec file.
