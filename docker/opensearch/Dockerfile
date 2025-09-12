FROM opensearchproject/opensearch:2.11.0

# Copy custom configuration
COPY opensearch.yml /usr/share/opensearch/config/
COPY jvm.options /usr/share/opensearch/config/

# Set proper permissions
USER root
RUN chown -R opensearch:opensearch /usr/share/opensearch/config/
USER opensearch

# Expose ports
EXPOSE 9200 9600
