FROM nginx:alpine

RUN apk update && apk upgrade && apk add --no-cache openssl

RUN mkdir /etc/nginx/ssl

RUN openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes \
                -out /etc/nginx/ssl/ft_transcendance.crt \
                -keyout /etc/nginx/ssl/ft_transcendance.key \
                -subj "/C=FR/ST=Lyon/L=Lyon/O=42 School/OU=ft_transcendance/CN=ft_transcendance/"

COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]