%define section         free
%define gcj_support     1

Name:           sleep
Version:        2.1.18
Release:        %mkrel 1
Epoch:          1
Summary:        A perl inspired embed-able scripting language for Java applications
License:        LGPL
URL:            http://sleep.hick.org/
Group:          Development/Java
#Vendor:        JPackage Project
#Distribution:  JPackage
Source0:        http://sleep.hick.org/download/sleep21b18.tgz
Patch0:         sleep-crosslink.patch
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-javadoc
BuildRequires:  jpackage-utils >= 0:1.5
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel >= 0:1.4.2
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Sleep is a perl inspired embed-able scripting language for Java 
applications. The main goals of sleep are easy to learn, easy to 
use, and easy to integrate.

Sleep source and binaries are released under the GNU Lesser General 
Public License History:

Sleep came from an inspired weekend of coding in April 2002. Since 
then Sleep has been developed in parallel with the Java IRC Client, 
jIRCii. Nearly three years later Sleep is a stable and ready to use 
solution for scripting Java applications. Features:

    * Perl inspired language syntax
    * Fast execution/small runtime size (160 KB)
    * Parsed scripts can be serialized
    * Easy API for making application data structures / functionality
      available to scripters
    * Full documentation for application developers and end-user scripters

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{ant} -Djava.javadoc=%{_javadocdir}/java jar docs-full

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
%{__rm} -rf docs/api

%{__perl} -pi -e 's/\r$//g' docs/parser.htm docs/common.htm license.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc license.txt readme.txt docs/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}

