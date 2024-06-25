FROM alpine:3.18    
COPY entrypoint.sh /entrypoint.sh 
RUN chmod +x /entrypoint.sh
COPY  cleanup.sh /cleanup.sh
RUN chmod +x /cleanup.sh
COPY setup.sh /setup.sh
RUN chmod +x /setup.sh

entrypoint ["/entrypoint.sh"]
CMD ["Hello"]