#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_CONFIG_MACRO_DIR([m4])
AC_INIT([f5gs],
	[m4_esyscmd([build-aux/git-version-gen .tarball-version])],
	[kerolasa@iki.fi], [],
	[https://github.com/kerolasa/f5gs])
PACKAGE_MAINTAINER="Sami Kerola"
AC_SUBST([PACKAGE_MAINTAINER])
AC_CONFIG_SRCDIR([f5gs.c])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_AUX_DIR([build-aux])
AM_INIT_AUTOMAKE([
	foreign
	1.11
	-Wall
	-Wextra-portability
	dist-xz
	no-dist-gzip
	subdir-objects
	tar-pax
])

# Checks for programs.
AC_USE_SYSTEM_EXTENSIONS
AC_C_RESTRICT
AC_PROG_CC
gl_EARLY
gl_INIT
LT_INIT

# Checks for libraries.
m4_ifndef([PKG_PROG_PKG_CONFIG],
  [m4_fatal([Could not locate the pkg-config autoconf
    macros. These are usually located in /usr/share/aclocal/pkg.m4.
    If your macros are in a different location, try setting the
    environment variable AL_OPTS="-I/other/macro/dir" before running
    ./autogen.sh or autoreconf again.])])
PKG_PROG_PKG_CONFIG

# Checks for header files.
AC_CHECK_HEADERS([arpa/inet.h fcntl.h netinet/in.h sys/socket.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_TYPE_SSIZE_T

# Checks for library functions.
AC_FUNC_MMAP
AC_CHECK_FUNCS([clearenv])

AC_ARG_ENABLE([systemd],
	AS_HELP_STRING([--enable-systemd], [build with systemd socket activation and use journald messages]),
	[enable_systemd=yes],
	[enable_systemd=no]
)
AM_CONDITIONAL([USE_SYSTEMD], [test "x$enable_systemd" = xyes])
AS_IF([test "x$enable_systemd" = xyes], [
	PKG_CHECK_MODULES([JOURNAL], [libsystemd-journal])
	AC_DEFINE([USE_SYSTEMD], [1], [use systemd socket activation])
])

AC_ARG_WITH([systemdsystemunitdir],
	AS_HELP_STRING([--with-systemdsystemunitdir=DIR], [directory for systemd service files]),
	[], [with_systemdsystemunitdir=`$PKG_CONFIG --variable=systemdsystemunitdir systemd`])

AS_IF([test "x$with_systemdsystemunitdir" != "xno"], [
	AC_SUBST([systemdsystemunitdir], [$with_systemdsystemunitdir])
])
AM_CONDITIONAL([HAVE_SYSTEMD],
	[test -n "$with_systemdsystemunitdir" -a "x$with_systemdsystemunitdir" != "xno"])

AC_DEFUN([DEFAULT_PORT], [32546])
AC_ARG_WITH([default-portl],
	[AS_HELP_STRING([--with-default-port=NUM], [default port (@<:@DEFAULT_PORT@:>@)])],
	[default_port="$withval"],
	[default_port="DEFAULT_PORT"])
AC_DEFINE_UNQUOTED([PORT_NUM], ["$default_port"], [default port])
AC_SUBST([PORT_NUM], [$default_port])

AC_SUBST([f5gs_post], [$sysconfdir/$PACKAGE/post], [f5gs signaling post])
AC_SUBST([f5gs_pre], [$sysconfdir/$PACKAGE/pre], [f5gs signaling pre])
AC_SUBST([f5gs_rundir], [$runstatedir/$PACKAGE/], [f5gs runtime state directory])

AC_CONFIG_FILES([Makefile
		lib/Makefile
])
AC_OUTPUT
