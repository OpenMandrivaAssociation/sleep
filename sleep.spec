%define section         free
%define gcj_support     1

Name:           sleep
Version:        2.1.26
Release:        %mkrel 0.0.1
Epoch:          1
Summary:        Perl inspired embedable scripting language for Java applications
License:        LGPL
URL:            http://sleep.hick.org/
Group:          Development/Java
Source0:        http://sleep.dashnine.org/download/sleep21b26.tgz
Patch0:         sleep-crosslink.patch
Patch1:         sleep-build.patch
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-javadoc
BuildRequires:  java-rpmbuild >= 0:1.5
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
    * Easy API for making application data structures/functionality
      available to scripters
    * Full documentation for application developers and end-user scripters

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%{__perl} -pi -e 's/\r$//g' docs/parser.htm docs/common.htm license.txt

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
%{__cp} -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc license.txt readme.txt whatsnew.txt docs/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}

