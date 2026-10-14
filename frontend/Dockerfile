# Используем стабильный LTS образ Node.js
FROM node:20-alpine

WORKDIR /app

# Копируем только файлы манифестов для кэширования
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY . .

CMD ["npm", "run", "dev"]