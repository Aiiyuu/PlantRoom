FROM node:20

WORKDIR /app

# Copy dependencies
COPY package.json package-lock.json /app/
RUN npm install

# Copy frontend files to the container
COPY . /app/

EXPOSE 8080

CMD ["npm", "run", "serve"]