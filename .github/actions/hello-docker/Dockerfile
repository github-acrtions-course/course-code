FROM alpine:3.18    
COPY entrypoint.sh /entrypoint.sh 
COPY  cleanup.sh /cleanup.sh
COPY setup.sh /setup.sh

entrypoint ["/entrypoint.sh"]
CMD ["Hello"]