FROM centos:7
ENV PORT 8000
ENV DOCROOT "/app"
RUN yum install -y httpd && \
    yum clean all

RUN sed -ri "/^Listen 80/c\Listen ${PORT}" /etc/httpd/conf/httpd.conf && \
    sed -ri "/^DocumentRoot */c\DocumentRoot \"${DOCROOT}\"\n<Directory \"/app\">\nAllowOverride None\nRequire all granted\n</Directory>" /etc/httpd/conf/httpd.conf && \
    usermod -u 1001 apache && mkdir ${DOCROOT} && chown -R root:root /app && \
    echo "<html><header><title>Hellow</title></header></html>" > /app/app.html
EXPOSE ${PORT}
CMD ["httpd", "-D", "FOREGROUND"]

