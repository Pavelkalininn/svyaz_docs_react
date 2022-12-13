FROM node:19

WORKDIR /app
COPY . .
COPY package*.json ./
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]