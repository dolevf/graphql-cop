# Use an official Node runtime as the base image
FROM node:14

# Set the working directory
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application files
COPY . .

# Expose the application port
EXPOSE 4000

# Start the server
CMD [ "npm", "start" ]
