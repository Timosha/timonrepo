RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

REPODIR := /home/timon/development/repo
RELEASE := 13
ARCH := x86_64

repo:
	ARCH := x86_64
	RELEASE := 13
	make arch
	ARCH := i386
	make arch
	ARCH := x86_64
	RELEASE := 12
	make arch
	ARCH := i386
	make arch

arch:	
	make mock && \
		mkdir -p $(REPODIR)/$(RELEASE)/{SRPMS,$(ARCH)} && \
		mkdir -p $(REPODIR)/$(RELEASE)/$(ARCH)/{os,debug} && \
		mv /var/lib/mock/fedora-$(RELEASE)-$(ARCH)/result/$(NAME)-debuginfo-*.rpm  $(REPODIR)/$(RELEASE)/$(ARCH)/debug && \
		mv /var/lib/mock/fedora-$(RELEASE)-$(ARCH)/result/$(NAME)-*.src.rpm  $(REPODIR)/$(RELEASE)/SRPMS && \
		mv /var/lib/mock/fedora-$(RELEASE)-$(ARCH)/result/$(NAME)-*.rpm  $(REPODIR)/$(RELEASE)/$(ARCH)/os && \
		cd $(REPODIR)/$(RELEASE)/$(ARCH)/os && createrepo --update . && \
		cd $(REPODIR)/$(RELEASE)/$(ARCH)/debug && createrepo --update . && \
		cd $(REPODIR)/$(RELEASE)/SRPMS && createrepo --update .

mock:
	make srpm
	mock -r fedora-$(RELEASE)-$(ARCH) rebuild $(NAME)*.src.rpm 

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 *.src.rpm

srpm:
	rpmbuild $(RPMDEFINES) -bs $(NAME).spec

build:
	rpmbuild $(RPMDEFINES) -bb $(NAME).spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

bc:
	rpmbuild $(RPMDEFINES) -bc --short-circuit $(NAME).spec

bi:
	rpmbuild $(RPMDEFINES) -bi --short-circuit $(NAME).spec

devbl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME)-dev.spec

bl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME).spec

devbuild:
	rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec

devbuildmini:
	rpmbuild $(RPMDEFINES) --define "runselftest 0" -bb $(NAME)-dev.spec

