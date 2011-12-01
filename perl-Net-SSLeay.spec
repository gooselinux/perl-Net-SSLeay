Name:		perl-Net-SSLeay
Version:	1.35
Release:	9%{?dist}
Summary:	Perl extension for using OpenSSL
Group:		Development/Libraries
License:	OpenSSL
URL:		http://search.cpan.org/dist/Net-SSLeay/
Source0:	http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/Net-SSLeay-%{version}.tar.gz
Patch0:		perl-Net-SSLeay-svn252.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker), openssl-devel
BuildRequires:	perl(MIME::Base64), perl(Sub::Uplevel)
BuildRequires:	perl(Test::Exception), perl(Test::NoWarnings), perl(Test::Pod)
BuildRequires:	perl(Test::Warn), perl(Tree::DAG_Node)

# don't "provide" private Perl libs or the redundant unversioned perl(Net::SSLeay) one
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
%global __find_provides /bin/sh -c "%{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P} | %{__grep} -Fvx 'perl(Net::SSLeay)'"
%global __find_requires /bin/sh -c "%{__deploop R}"

%description
This module offers some high level convenience functions for accessing
web pages on SSL servers (for symmetry, same API is offered for
accessing http servers, too), a sslcat() function for writing your own
clients, and finally access to the SSL api of SSLeay/OpenSSL package
so you can write servers or clients for more complicated applications.

%prep
%setup -q -n Net-SSLeay-%{version}

# Upstream patch removing MD2 support, needed for OpenSSL 1.0
%patch0

%{__chmod} -c 644 examples/*
%{__perl} -pi -e 's|/usr/local/bin/perl|%{__perl}|' examples/*.pl
for f in Credits lib/Net/SSLeay.pm; do
	/usr/bin/iconv -f iso-8859-1 -t utf-8 ${f} > ${f}.utf8
	%{__mv} ${f}.utf8 ${f}
done

%build
PERL_MM_USE_DEFAULT=1 %{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	INC="$(/usr/bin/pkg-config --cflags-only-I openssl)" \
	LIBS="$(/usr/bin/pkg-config --libs openssl)" \
	OPTIMIZE="%{optflags}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -type f -name '*.bs' -empty -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
%{__rm} -f %{buildroot}%{perl_vendorarch}/Net/ptrtstrun.pl
%{__chmod} -R u+w %{buildroot}/*

%check
%{__make} test TEST_VERBOSE=1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes Credits QuickRef README examples/ TODO
%{perl_vendorarch}/auto/Net/
%{perl_vendorarch}/Net/
%{_mandir}/man3/Net::SSLeay*.3*

%changelog
* Tue Dec 22 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.35-9
- we don't need Array::Compare anymore
- Resolves: rhbz#549733

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.35-8
- rebuild against perl 5.10.1

* Sat Aug 22 2009 Paul Howarth <paul@city-fan.org> - 1.35-7
- update to svn trunk (rev 252), needed due to omission of MD2 functionality
  from OpenSSL 1.0.0 (CPAN RT#48916)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.35-6
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-5
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar  8 2009 Paul Howarth <paul@city-fan.org> - 1.35-4
- filter out unwanted provides for perl shared objects
- run tests in verbose mode

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.35-2
- rebuild with new openssl

* Mon Jul 28 2008 Paul Howarth <paul@city-fan.org> - 1.35-1
- update to 1.35
- drop flag and patch for enabling/disabling external tests - patch now upstream
- external hosts patch no longer needed as we don't do external tests
- filter out unversioned provide for perl(Net::SSLeay)
- use the distro openssl flags rather than guessing them

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.32-5
- rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.32-4
- autorebuild for GCC 4.3

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.32-3
- rebuild for new perl

* Wed Dec  5 2007 Paul Howarth <paul@city-fan.org> - 1.32-2
- rebuild with new openssl

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.32-1
- update to 1.32, incorporate new upstream URLs
- cosmetic spec changes suiting new maintainer's preferences
- fix argument order for find with -depth
- remove patch for CVE-2005-0106, fixed upstream in 1.30 (#191351)
  (http://rt.cpan.org/Public/Bug/Display.html?id=19218)
- remove test patch, no longer needed
- re-encode Credits as UTF-8
- include TODO as %%doc
- add buildreqs perl(Array::Compare), perl(MIME::Base64), perl(Sub::Uplevel),
  perl(Test::Exception), perl(Test::NoWarnings), perl(Test::Pod),
  perl(Test::Warn), perl(Tree::DAG_Node)
- add patch needed to disable testsuite non-interactively
- run test suite but disable external tests by default; external tests can be
  enabled by using rpmbuild --with externaltests
- add patch to change hosts connected to in external tests

* Fri Nov 16 2007 Parag Nemade <panemade@gmail.com> - 1.30-7
- Merge Review (#226272) Spec cleanup

* Tue Nov  6 2007 Stepan Kasal <skasal@redhat.com> - 1.30-6
- fix a typo in description (#231756, #231757)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.30-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> - 1.30-5
- rebuild

* Fri Jul 14 2006 Warren Togami <wtogami@redhat.com> - 1.30-4
- import into FC6

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.30-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Jan 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.30-2
- CVE-2005-0106: patch from Mandriva
  http://wwwnew.mandriva.com/security/advisories?name=MDKSA-2006:023

* Sun Jan 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.30-1
- 1.30.
- Optionally run the test suite during build with "--with tests".

* Wed Nov  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.26-3
- Rebuild for new OpenSSL.
- Cosmetic cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.26-2
- rebuilt

* Mon Dec 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.26-1
- Drop fedora.us release prefix and suffix.

* Mon Oct 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.26-0.fdr.2
- Convert manual page to UTF-8.

* Tue Oct 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.26-0.fdr.1
- Update to unofficial 1.26 from Peter Behroozi, adds get1_session(),
  enables session caching with IO::Socket::SSL (bug 1859, bug 1860).
- Bring outdated test14 up to date (bug 1859, test suite still not enabled).

* Sun Jul 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.4
- Rename to perl-Net-SSLeay, provide perl-Net_SSLeay for compatibility
  with the rest of the world.

* Wed Jul  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.3
- Bring up to date with current fedora.us Perl spec template.
- Include examples in docs.

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.2
- Reduce directory ownership bloat.

* Fri Oct 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.1
- First build.
