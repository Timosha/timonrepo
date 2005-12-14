/*
 * Kluge to support multilib installation of both 32- and 64-bit RPMS:
 * we need to arrange that header files that appear in both RPMs are
 * identical.  Hence, this file is architecture-independent and calls
 * in an arch-dependent file that will appear in just one RPM.
 *
 * Note: this may well fail if user tries to use gcc's -I- option.
 * But that option is deprecated anyway.
 */
#ifdef __i386__
#include "pg_config_i386.h"
#endif
#ifdef __x86_64__
#include "pg_config_x86_64.h"
#endif
#ifdef __ia64__
#include "pg_config_ia64.h"
#endif
#ifdef __ppc__
#include "pg_config_ppc.h"
#endif
#ifdef __ppc64__
#include "pg_config_ppc64.h"
#endif
#ifdef __s390__
#include "pg_config_s390.h"
#endif
#ifdef __s390x__
#include "pg_config_s390x.h"
#endif
