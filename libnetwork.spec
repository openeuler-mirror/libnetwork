%define  debug_package %{nil}
Name: libnetwork
Version: 0.8.0.dev.2
Release: 105
Summary: Proxy used for docker port mapping
License: CC-BY-SA-4.0 and MIT and Apache-2.0 and MPL-2.0
URL: https://github.com/docker/libnetwork
Source: libnetwork-d00ceed.tar.gz
BuildRequires: golang >= 1.8.3
BuildRequires: make
Provides: docker-proxy
Obsoletes: docker-proxy

%description

%prep
%setup -c -n libnetwork

%build
cd libnetwork-d00ceed44cc447c77f25cdf5d59e83163bdcb4c9
export GO111MODULE=off
export CGO_ENABLED=0
export GOPATH=`pwd`/.gopath
mkdir -p $GOPATH/src/github.com/docker/
ln -sfn `pwd` $GOPATH/src/github.com/docker/libnetwork
cd $GOPATH/src/github.com/docker/libnetwork
CGO_ENABLED=1 \
CGO_CFLAGS="-fstack-protector-strong -fPIE" \
CGO_CPPFLAGS="-fstack-protector-strong -fPIE" \
CGO_LDFLAGS_ALLOW='-Wl,-z,relro,-z,now' \
CGO_LDFLAGS="-Wl,-z,relro,-z,now -Wl,-z,noexecstack" \
%if "%toolchain" == "clang"
	go build -buildmode=pie -ldflags="-linkmode=external -s -w -buildid=IdByIsula " -o docker-proxy ./cmd/proxy
%else 
	go build -buildmode=pie -ldflags="-linkmode=external -s -w -buildid=IdByIsula -extldflags=-zrelro -extldflags=-znow " -o docker-proxy ./cmd/proxy
%endif

%install
install -d $RPM_BUILD_ROOT/%{_bindir}
install -p -m 755 libnetwork-d00ceed44cc447c77f25cdf5d59e83163bdcb4c9/docker-proxy $RPM_BUILD_ROOT/%{_bindir}/docker-proxy

%clean
%{__rm} -rf %{_bindir}/docker-proxy

%files
%{_bindir}/docker-proxy

%changelog
* Sat May 06 2023 yoo <sunyuechi@iscas.ac.cn> - 0.8.0.dev.2-105
- fix clang build error

* Fri May 20 2022 liukuo <liukuo@kylinos.cn> - 0.8.0.dev.2-104
- License compliance rectification

* Mon Jan 10 2022 xiadanni<xiadanni1@huawei.com> 0.8.0.dev.2-103
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:disable go module build

* Thu Mar 18 2021 xiadanni<xiadanni1@huawei.com> 0.8.0.dev.2-102
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:compile option compliance

* Thu Aug 20 2020 xiadanni<xiadanni1@huawei.com> 0.8.0.dev.2-101
- Type:cleancode
- Id:NA
- SUG:NA
- DESC:modify source code struct

* Mon Sep 30 2019 songnannan<songnannan2@huawei.com> 0.8.0.dev.2-2.h1
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:the debuginfo and debugsource packages are not generated by default
