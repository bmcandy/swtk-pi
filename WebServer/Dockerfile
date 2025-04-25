# Use an official PHP image as the base image
FROM php:apache

# Install php-mysqli extension
RUN docker-php-ext-install mysqli

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy the contents of the WebServer folder into the container
COPY . /var/www/html

# Expose port 80 for the web server
EXPOSE 80

# Set the default command to run the Apache server
CMD ["apache2-foreground"]