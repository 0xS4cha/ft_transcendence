#!/bin/sh

if [ -n "$PROMETHEUS_ADMIN_USER" ] && [ -n "$PROMETHEUS_ADMIN_PASSWORD" ]; then
    htpasswd -cb /etc/nginx/.htpasswd "$PROMETHEUS_ADMIN_USER" "$PROMETHEUS_ADMIN_PASSWORD"
else
    exit 1
fi
exec nginx -g "daemon off;"
