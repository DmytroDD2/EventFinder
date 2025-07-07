# Build Stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json yarn.lock ./

RUN set -eux \
    & apk add \
        --no-cache \
        yarn 
COPY . .
RUN yarn run build

# Production Stage
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]