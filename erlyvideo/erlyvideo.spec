# FIXME
%global debug_package %{nil}
%global git_tag 25cf0c2


Name:		erlyvideo
Version:	2.5.11
Release:	1%{?dist}
Summary:	Erlang RTMP server
Group:		Applications/Multimedia
License:	GPLv3
URL:		http://erlyvideo.org/
# wget http://github.com/erlyvideo/erlyvideo/tarball/v2.5.11
Source0:	erlyvideo-%{name}-v%{version}-0-g%{git_tag}.tar.gz
# wget http://github.com/erlyvideo/erlyplayer/tarball/eed2837
Source1:	erlyvideo-erlyplayer-eed2837.tar.gz
Patch1:		erlyvideo-0001-Fix-install-section.patch
Patch2:		erlyvideo-0002-Fix-path-to-init-script-Fedora-RHEL-specific.patch
Patch3:		erlyvideo-0003-Install-only-necessary-files.patch
Patch4:		erlyvideo-0004-Fix-installing-of-contributed-rtmp-apps.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	erlang
BuildRequires:	ruby
Requires:	erlang

BuildRequires:	fedora-usermgmt-devel
%{?FE_USERADD_REQ}

Requires(post):		/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service

%description
Erlang RTMP server.


%prep
%setup -q -n erlyvideo-erlyvideo-1cf9504
mkdir -p wwwroot/player
tar xf %{SOURCE1} --strip-components=1 -C wwwroot/player/
%patch1 -p1 -b .install
%patch2 -p1 -b .init-path
%patch3 -p1 -b .only_required
%patch4 -p1 -b .install_rtmp_contribs


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTROOT=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/lib/erlydtl-%{version}/src
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/lib/log4erl-%{version}/src


%clean
rm -rf $RPM_BUILD_ROOT

%pre
%{__fe_groupadd} -r %{name} &>/dev/null || :
%{__fe_useradd} -r -s /sbin/nologin -d %{_sharedstatedir}/%{name} -M \
			-c '%{name}' -g %{name} %{name} &>/dev/null || :

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%post
/sbin/chkconfig --add %{name}

%files
%defattr(-,root,root,-)
%doc
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/log4erl.conf
%config(noreplace) %{_sysconfdir}/%{name}/production.config
%{_initrddir}/%{name}
%{_bindir}/erlyctl
%{_bindir}/reverse_mpegts
%{_bindir}/rtmp_bench
%{_bindir}/so_bench

# amf
%dir %{_libdir}/erlang/lib/amf-%{version}
%dir %{_libdir}/erlang/lib/amf-%{version}/ebin
%{_libdir}/erlang/lib/amf-%{version}/ebin/amf0.beam
%{_libdir}/erlang/lib/amf-%{version}/ebin/amf0_tests.beam
%{_libdir}/erlang/lib/amf-%{version}/ebin/amf3.beam
%{_libdir}/erlang/lib/amf-%{version}/ebin/amf3_tests.beam
%{_libdir}/erlang/lib/amf-%{version}/ebin/eamf.app

# erlmedia
%dir %{_libdir}/erlang/lib/erlmedia-%{version}
%dir %{_libdir}/erlang/lib/erlmedia-%{version}/ebin
%dir %{_libdir}/erlang/lib/erlmedia-%{version}/include
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/aac.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/ems_log.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/erlmedia.app
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/flv.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/flv_reader.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/flv_video_frame.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/flv_writer.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/gen_format.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/gen_listener.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/h264.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/http_uri2.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/http_stream.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/jpeg_reader.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mjpeg_reader.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mkv.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mp3.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mp3_reader.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mp4.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mp4_reader.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/mp4_writer.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/packet_codec.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/shoutcast_reader.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/srt_parser.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/ebin/wav.beam
%{_libdir}/erlang/lib/erlmedia-%{version}/include/aac.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/flv.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/h264.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/mp3.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/mp4.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/srt.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/video_frame.hrl
%{_libdir}/erlang/lib/erlmedia-%{version}/include/wav.hrl

# ErlyDTL
%dir %{_libdir}/erlang/lib/erlydtl-%{version}
%dir %{_libdir}/erlang/lib/erlydtl-%{version}/ebin
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_compiler.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_dateformat.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_dateformat_tests.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_deps.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_example_variable_storage.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_filters.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_functional_tests.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_parser.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_runtime.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_scanner.beam
%{_libdir}/erlang/lib/erlydtl-%{version}/ebin/erlydtl_unittests.beam

# erlyvideo
%dir %{_libdir}/erlang/lib/%{name}-%{version}
%dir %{_libdir}/erlang/lib/%{name}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{name}-%{version}/include
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/%{name}.app
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{name}-%{version}/include/erlyvideo.hrl
#%{_libdir}/erlang/lib/%{name}-%{version}/include/ERLYVIDEO-MIB.hrl
%{_libdir}/erlang/lib/%{name}-%{version}/include/ems_media.hrl
%{_libdir}/erlang/lib/%{name}-%{version}/include/rtmp_session.hrl

# log4erl
%dir %{_libdir}/erlang/lib/log4erl-%{version}
%dir %{_libdir}/erlang/lib/log4erl-%{version}/ebin
%dir %{_libdir}/erlang/lib/log4erl-%{version}/include
%{_libdir}/erlang/lib/log4erl-%{version}/ebin/log4erl.app
%{_libdir}/erlang/lib/log4erl-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/log4erl-%{version}/include/log4erl.hrl

# mpegts
%dir %{_libdir}/erlang/lib/mpegts-%{version}
%dir %{_libdir}/erlang/lib/mpegts-%{version}/ebin
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/ems_http_mpegts.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/iphone_streams.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpeg2_crc32.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpeg2_crc32.so
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts.app
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts_file_reader.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts_play.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts_reader.beam
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts_reader.so
%{_libdir}/erlang/lib/mpegts-%{version}/ebin/mpegts_sup.beam

# rtmp
%dir %{_libdir}/erlang/lib/rtmp-%{version}
%dir %{_libdir}/erlang/lib/rtmp-%{version}/ebin
%dir %{_libdir}/erlang/lib/rtmp-%{version}/include
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/hmac256.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp.app
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_app.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_bench.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_handshake.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_handshake_tests.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_lib.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_listener.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_socket.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_stat_collector.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmp_sup.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmpe.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/rtmpt.beam
%{_libdir}/erlang/lib/rtmp-%{version}/ebin/sha2.beam
%{_libdir}/erlang/lib/rtmp-%{version}/include/rtmp.hrl

# rtp
%dir %{_libdir}/erlang/lib/rtp-%{version}
%dir %{_libdir}/erlang/lib/rtp-%{version}/ebin
%dir %{_libdir}/erlang/lib/rtp-%{version}/include
%{_libdir}/erlang/lib/rtp-%{version}/ebin/ertp.app
%{_libdir}/erlang/lib/rtp-%{version}/ebin/ertp.beam
%{_libdir}/erlang/lib/rtp-%{version}/ebin/ertp_sup.beam
%{_libdir}/erlang/lib/rtp-%{version}/ebin/rtp_server.beam
%{_libdir}/erlang/lib/rtp-%{version}/ebin/sdp.beam
%{_libdir}/erlang/lib/rtp-%{version}/ebin/sdp_tests.beam
%{_libdir}/erlang/lib/rtp-%{version}/include/sdp.hrl

# rtsp
%dir %{_libdir}/erlang/lib/rtsp-%{version}
%dir %{_libdir}/erlang/lib/rtsp-%{version}/ebin
%dir %{_libdir}/erlang/lib/rtsp-%{version}/include
%{_libdir}/erlang/lib/rtsp-%{version}/ebin/rtsp.app
%{_libdir}/erlang/lib/rtsp-%{version}/ebin/rtsp.beam
%{_libdir}/erlang/lib/rtsp-%{version}/ebin/rtsp_example_callback.beam
%{_libdir}/erlang/lib/rtsp-%{version}/ebin/rtsp_listener.beam
%{_libdir}/erlang/lib/rtsp-%{version}/ebin/rtsp_socket.beam
%{_libdir}/erlang/lib/rtsp-%{version}/ebin/rtsp_sup.beam
%{_libdir}/erlang/lib/rtsp-%{version}/include/rtsp.hrl
%{_libdir}/erlang/lib/rtsp-%{version}/include/sdp.hrl

/var/lib/erlyvideo

%changelog
* Sat Oct 30 2010 Timon <timosha@gmail.com> - 2.4.13-2
- add user and group
- fix init.d script add

* Sat Oct 30 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.4.13-1
- Initial build
