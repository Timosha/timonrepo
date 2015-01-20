RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

REPODIR := /home/timon/development/repo
RELEASE := 20
ARCH := x86_64

build: prep
	rpmbuild $(RPMDEFINES) -bb $(NAME).spec

prep: 
	spectool -g -S $(NAME).spec

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 *.src.rpm

srpm: prep
	rpmbuild $(RPMDEFINES) -bs $(NAME).spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

bc:
	rpmbuild $(RPMDEFINES) -bc --short-circuit $(NAME).spec

bi:
	rpmbuild $(RPMDEFINES) -bi --short-circuit $(NAME).spec

bl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME).spec


mock: clean srpm
	mock -r fedora-$(RELEASE)-$(ARCH) rebuild $(NAME)*.src.rpm 

repo: clean f19 f18

f21: f21-x86_64

f20: f20-x86_64

f19: f19-x86_64

f18: f18-x86_64 f18-i386

f17: f17-x86_64 f17-i386

f16: f16-x86_64 f16-i386

f15: f15-x86_64 f15-i386

f14: f14-x86_64 f14-i386

f13: f13-x86_64 f13-i386

arch: clean f$(RELEASE)-$(ARCH)

f21-x86_64: srpm
	mock -r fedora-21-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/21/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/21/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-21-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/21/x86_64/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-21-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/21/SRPMS && \
	mv /var/lib/mock/fedora-21-x86_64/result/*-*.rpm  $(REPODIR)/21/x86_64/os && \
	cd $(REPODIR)/21/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/21/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/21/SRPMS && createrepo --update .

f20-x86_64: srpm
	mock -r fedora-20-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/20/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/20/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-20-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/20/x86_64/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-20-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/20/SRPMS && \
	mv /var/lib/mock/fedora-20-x86_64/result/*-*.rpm  $(REPODIR)/20/x86_64/os && \
	cd $(REPODIR)/20/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/20/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/20/SRPMS && createrepo --update .

f19-x86_64: srpm
	mock -r fedora-19-x86_64 rebuild $(NAME)*.src.rpm && \
        mkdir -p $(REPODIR)/19/{SRPMS,x86_64} && \
        mkdir -p $(REPODIR)/19/x86_64/{os,debug} && \
        ( mv /var/lib/mock/fedora-19-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/19/x86_64/debug || echo noarch ) && \
        mv /var/lib/mock/fedora-19-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/19/SRPMS && \
        mv /var/lib/mock/fedora-19-x86_64/result/*-*.rpm  $(REPODIR)/19/x86_64/os && \
        cd $(REPODIR)/19/x86_64/os && createrepo --update . && \
        cd $(REPODIR)/19/x86_64/debug && createrepo --update . && \
        cd $(REPODIR)/19/SRPMS && createrepo --update .

f18-x86_64: srpm
	mock -r fedora-18-x86_64 rebuild $(NAME)*.src.rpm && \
        mkdir -p $(REPODIR)/18/{SRPMS,x86_64} && \
        mkdir -p $(REPODIR)/18/x86_64/{os,debug} && \
        ( mv /var/lib/mock/fedora-18-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/18/x86_64/debug || echo noarch ) && \
        mv /var/lib/mock/fedora-18-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/18/SRPMS && \
        mv /var/lib/mock/fedora-18-x86_64/result/*-*.rpm  $(REPODIR)/18/x86_64/os && \
        cd $(REPODIR)/18/x86_64/os && createrepo --update . && \
        cd $(REPODIR)/18/x86_64/debug && createrepo --update . && \
        cd $(REPODIR)/18/SRPMS && createrepo --update .

f18-i386: srpm
	mock -r fedora-18-i386 rebuild $(NAME)*.src.rpm && \
        mkdir -p $(REPODIR)/18/{SRPMS,i386} && \
        mkdir -p $(REPODIR)/18/i386/{os,debug} && \
        ( mv /var/lib/mock/fedora-18-i386/result/*-debuginfo-*.rpm  $(REPODIR)/18/i386/debug || echo noarch) && \
        mv /var/lib/mock/fedora-18-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/18/SRPMS && \
        mv /var/lib/mock/fedora-18-i386/result/*-*.rpm  $(REPODIR)/18/i386/os && \
        cd $(REPODIR)/18/i386/os && createrepo --update . && \
        cd $(REPODIR)/18/i386/debug && createrepo --update . && \
        cd $(REPODIR)/18/SRPMS && createrepo --update .

f17-x86_64: srpm
	mock -r fedora-17-x86_64 rebuild $(NAME)*.src.rpm && \
        mkdir -p $(REPODIR)/17/{SRPMS,x86_64} && \
        mkdir -p $(REPODIR)/17/x86_64/{os,debug} && \
        ( mv /var/lib/mock/fedora-17-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/17/x86_64/debug || echo noarch ) && \
        mv /var/lib/mock/fedora-17-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/17/SRPMS && \
        mv /var/lib/mock/fedora-17-x86_64/result/*-*.rpm  $(REPODIR)/17/x86_64/os && \
        cd $(REPODIR)/17/x86_64/os && createrepo --update . && \
        cd $(REPODIR)/17/x86_64/debug && createrepo --update . && \
        cd $(REPODIR)/17/SRPMS && createrepo --update .

f17-i386: srpm
	mock -r fedora-17-i386 rebuild $(NAME)*.src.rpm && \
        mkdir -p $(REPODIR)/17/{SRPMS,i386} && \
        mkdir -p $(REPODIR)/17/i386/{os,debug} && \
        ( mv /var/lib/mock/fedora-17-i386/result/*-debuginfo-*.rpm  $(REPODIR)/17/i386/debug || echo noarch) && \
        mv /var/lib/mock/fedora-17-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/17/SRPMS && \
        mv /var/lib/mock/fedora-17-i386/result/*-*.rpm  $(REPODIR)/17/i386/os && \
        cd $(REPODIR)/17/i386/os && createrepo --update . && \
        cd $(REPODIR)/17/i386/debug && createrepo --update . && \
        cd $(REPODIR)/17/SRPMS && createrepo --update .

f16-x86_64: srpm
	mock -r fedora-16-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/16/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/16/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-16-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/16/x86_64/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-16-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/16/SRPMS && \
	mv /var/lib/mock/fedora-16-x86_64/result/*-*.rpm  $(REPODIR)/16/x86_64/os && \
	cd $(REPODIR)/16/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/16/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/16/SRPMS && createrepo --update .

f16-i386: srpm
	mock -r fedora-16-i386 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/16/{SRPMS,i386} && \
	mkdir -p $(REPODIR)/16/i386/{os,debug} && \
	( mv /var/lib/mock/fedora-16-i386/result/*-debuginfo-*.rpm  $(REPODIR)/16/i386/debug || echo noarch) && \
	mv /var/lib/mock/fedora-16-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/16/SRPMS && \
	mv /var/lib/mock/fedora-16-i386/result/*-*.rpm  $(REPODIR)/16/i386/os && \
	cd $(REPODIR)/16/i386/os && createrepo --update . && \
	cd $(REPODIR)/16/i386/debug && createrepo --update . && \
	cd $(REPODIR)/16/SRPMS && createrepo --update .

f15-x86_64: srpm
	mock -r fedora-15-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/15/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/15/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-15-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/15/x86_64/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-15-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/15/SRPMS && \
	mv /var/lib/mock/fedora-15-x86_64/result/*-*.rpm  $(REPODIR)/15/x86_64/os && \
	cd $(REPODIR)/15/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/15/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/15/SRPMS && createrepo --update .

f15-i386: srpm
	mock -r fedora-15-i386 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/15/{SRPMS,i386} && \
	mkdir -p $(REPODIR)/15/i386/{os,debug} && \
	( mv /var/lib/mock/fedora-15-i386/result/*-debuginfo-*.rpm  $(REPODIR)/15/i386/debug || echo noarch) && \
	mv /var/lib/mock/fedora-15-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/15/SRPMS && \
	mv /var/lib/mock/fedora-15-i386/result/*-*.rpm  $(REPODIR)/15/i386/os && \
	cd $(REPODIR)/15/i386/os && createrepo --update . && \
	cd $(REPODIR)/15/i386/debug && createrepo --update . && \
	cd $(REPODIR)/15/SRPMS && createrepo --update .

f14-x86_64: srpm
	mock -r fedora-14-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/14/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/14/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-14-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/14/x86_64/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-14-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/14/SRPMS && \
	mv /var/lib/mock/fedora-14-x86_64/result/*-*.rpm  $(REPODIR)/14/x86_64/os && \
	cd $(REPODIR)/14/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/14/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/14/SRPMS && createrepo --update .

f14-i386: srpm
	mock -r fedora-14-i386 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/14/{SRPMS,i386} && \
	mkdir -p $(REPODIR)/14/i386/{os,debug} && \
	( mv /var/lib/mock/fedora-14-i386/result/*-debuginfo-*.rpm  $(REPODIR)/14/i386/debug || echo noarch) && \
	mv /var/lib/mock/fedora-14-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/14/SRPMS && \
	mv /var/lib/mock/fedora-14-i386/result/*-*.rpm  $(REPODIR)/14/i386/os && \
	cd $(REPODIR)/14/i386/os && createrepo --update . && \
	cd $(REPODIR)/14/i386/debug && createrepo --update . && \
	cd $(REPODIR)/14/SRPMS && createrepo --update .


f13-x86_64: srpm
	mock -r fedora-13-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/13/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/13/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-13-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/13/x86_64/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-13-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/13/SRPMS && \
	mv /var/lib/mock/fedora-13-x86_64/result/*-*.rpm  $(REPODIR)/13/x86_64/os && \
	cd $(REPODIR)/13/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/13/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/13/SRPMS && createrepo --update .

f13-i386: srpm
	mock -r fedora-13-i386 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/13/{SRPMS,i386} && \
	mkdir -p $(REPODIR)/13/i386/{os,debug} && \
	( mv /var/lib/mock/fedora-13-i386/result/*-debuginfo-*.rpm  $(REPODIR)/13/i386/debug || echo noarch) && \
	mv /var/lib/mock/fedora-13-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/13/SRPMS && \
	mv /var/lib/mock/fedora-13-i386/result/*-*.rpm  $(REPODIR)/13/i386/os && \
	cd $(REPODIR)/13/i386/os && createrepo --update . && \
	cd $(REPODIR)/13/i386/debug && createrepo --update . && \
	cd $(REPODIR)/13/SRPMS && createrepo --update .

f12-x86_64: srpm
	mock -r fedora-12-x86_64 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/12/{SRPMS,x86_64} && \
	mkdir -p $(REPODIR)/12/x86_64/{os,debug} && \
	( mv /var/lib/mock/fedora-12-x86_64/result/*-debuginfo-*.rpm  $(REPODIR)/12/x86_64/debug || echo noarch) && \
	mv /var/lib/mock/fedora-12-x86_64/result/$(NAME)-*.src.rpm  $(REPODIR)/12/SRPMS && \
	mv /var/lib/mock/fedora-12-x86_64/result/*-*.rpm  $(REPODIR)/12/x86_64/os && \
	cd $(REPODIR)/12/x86_64/os && createrepo --update . && \
	cd $(REPODIR)/12/x86_64/debug && createrepo --update . && \
	cd $(REPODIR)/12/SRPMS && createrepo --update .

f12-i386: srpm	
	mock -r fedora-12-i386 rebuild $(NAME)*.src.rpm && \
	mkdir -p $(REPODIR)/12/{SRPMS,i386} && \
	mkdir -p $(REPODIR)/12/i386/{os,debug} && \
	( mv /var/lib/mock/fedora-12-i386/result/*-debuginfo-*.rpm  $(REPODIR)/12/i386/debug || echo noarch ) && \
	mv /var/lib/mock/fedora-12-i386/result/$(NAME)-*.src.rpm  $(REPODIR)/12/SRPMS && \
	mv /var/lib/mock/fedora-12-i386/result/*-*.rpm  $(REPODIR)/12/i386/os && \
	cd $(REPODIR)/12/i386/os && createrepo --update . && \
	cd $(REPODIR)/12/i386/debug && createrepo --update . && \
	cd $(REPODIR)/12/SRPMS && createrepo --update .


