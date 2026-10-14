# Estágio 1: Build do React
FROM node:22-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN echo "Instalando depêndencias do Node"
RUN npm install

COPY . .
RUN echo "Iniciando Build........."
RUN npm run build

# Estágio 2: Servir com Nginx
FROM nginx:alpine
# Copia o build do React para a pasta estática do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copia arquivo de configuração customizado do Nginx para suportar rotas de SPA
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]