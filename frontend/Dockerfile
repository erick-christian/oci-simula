FROM node:18-alpine

WORKDIR /app

# Copiamos solo el package.json primero para aprovechar el caché
COPY package.json .

# Instalamos dependencias
RUN npm install

# Copiamos el resto de los archivos
COPY . .

# Exponemos el puerto de Vite
EXPOSE 5173

# Comando de inicio
CMD ["npm", "run", "dev", "--", "--host"]