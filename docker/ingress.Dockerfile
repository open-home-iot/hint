FROM docker.io/nginx:1.23.1

COPY nginx/ingress/nginx.conf /etc/nginx/nginx.conf
COPY backend/static/collectedstatic /data/static
