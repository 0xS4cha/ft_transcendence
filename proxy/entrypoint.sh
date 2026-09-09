#!/bin/sh
echo "test1"
if [ -n "$PROMETHEUS_ADMIN_USER" ] && [ -n "$PROMETHEUS_ADMIN_PASSWORD" ]; then
    echo "test2"
    htpasswd -cb /etc/nginx/.htpasswd "$PROMETHEUS_ADMIN_USER" "$PROMETHEUS_ADMIN_PASSWORD"
else
    echo "test3"
    exit 1
fi
echo "test4"
exec nginx -g "daemon off;"
