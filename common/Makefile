RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

REPODIR := /home/timon/development/repo
RELEASE := 13
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


mock: srpm
	mock -r fedora-$(RELEASE)-$(ARCH) rebuild $(NAME)*.src.rpm 

repo: f13 f12

f13: f13-x86_64 f13-i386

f12: f12-x86_64 f12-i386

arch:	f$(RELEASE)-$(ARCH)

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


