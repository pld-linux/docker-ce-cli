Summary:	The Docker CLI
Name:		docker-ce-cli
Version:	28.0.1
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	https://github.com/docker/cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	931f32ae5b5525e4aae1a12a6dc9af87
URL:		https://www.docker.com/
BuildRequires:	golang >= 1.12
BuildRequires:	rpmbuild(macros) >= 2.009
Suggests:	docker(engine) >= 20.10.1
Suggests:	docker-credential-helpers
Suggests:	git-core >= 1.7
Obsoletes:	bash-completion-docker-ce < 27.1.2
Obsoletes:	bash-completion-lxc-docker < 1.1.1
Obsoletes:	zsh-completion-docker-ce < 27.1.2
Conflicts:	docker-ce < 20.10.1
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0

%description
The Docker CLI.

%prep
%setup -q -c -T -n %{name}-%{version}/src/github.com/docker/cli
tar xf %{SOURCE0} --strip-components=1

%build
export VERSION=%{version}
export GITCOMMIT="PLD-Linux/%{version}"
export GO111MODULE=off

GOPATH=$(pwd)/../../../.. \
DISABLE_WARN_OUTSIDE_CONTAINER=1 \
%{__make} dynbinary
./build/docker -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libexecdir}/docker/cli-plugins}

# docker-cli
install -p build/docker $RPM_BUILD_ROOT%{_bindir}/docker

# bash and zsh completion
cd contrib/completion
install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p bash/docker $RPM_BUILD_ROOT%{bash_compdir}
install -d $RPM_BUILD_ROOT%{zsh_compdir}
cp -p zsh/_docker $RPM_BUILD_ROOT%{zsh_compdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/docker
%dir %{_libexecdir}/docker
%dir %{_libexecdir}/docker/cli-plugins
%{bash_compdir}/docker
%{zsh_compdir}/_docker
