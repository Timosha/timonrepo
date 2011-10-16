#include <libhashkit/common.h>

#ifdef HAVE_HSIEH_HASH
#error "not supported"
#else
uint32_t hashkit_hsieh(const char *, size_t , void *) { return 0; }
#endif
