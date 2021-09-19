Name:		fake-hwclock
Version:	0.9
Release:	1%{?dist}
Summary:	Save/restore system clock on machines without working RTC hardware

License:	GPLv2
URL:            http://git.einval.com/cgi-bin/gitweb.cgi?p=fake-hwclock.git
# git clone http://git.einval.com/git/fake-hwclock.git
# cd fake-hwclock
# git archive --format=tar.gz --prefix=fake-hwclock-0.9/ v0.9 > ../fake-hwclock-0.9.tar.gz
Source0:	%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
Some machines don't have a working realtime clock (RTC) unit, or no driver
for the hardware that does exist. fake-hwclock is a simple set of scripts to
save the kernel's current clock periodically (including at shutdown) and
restore it at boot so that the system clock keeps at least close to realtime.
This will stop some of the problems that may be caused by a system believing
it has travelled in time back to 1970, such as needing to perform filesystem
checks at every boot.

On top of this, use of NTP is still recommended to deal with the fake clock
"drifting" while the hardware is halted or rebooting. 

%prep
%setup -q


%build


%install
install -D -m 755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -m 644 %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8
install -D -m 644 etc/default/%{name} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 debian/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
touch %{buildroot}%{_sysconfdir}/%{name}.data


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license COPYING
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}*
%config(noreplace) %{_sysconfdir}/default/%{name}
%ghost %{_sysconfdir}/%{name}.data
%{_unitdir}/%{name}.service


%changelog
* Fri Jun 05 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.9-1
- Initial release.
