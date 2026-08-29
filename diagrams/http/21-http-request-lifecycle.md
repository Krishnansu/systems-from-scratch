# What Happens When You Type http://example.com

```text
You type:

http://example.com
        │
        ▼
     Browser
        │
        │ DNS lookup
        ▼
  IP Address Found
        │
        ▼
 TCP Three-Way Handshake
        │
        ▼
  TCP Connection Ready
        │
        ▼
  Browser creates
    HTTP Request
        │
        ▼
  HTTP bytes given
       to TCP
        │
        ▼
    TCP Segments
        │
        ▼
    IP Packets
        │
        ▼
      Network
        │
        ▼
      Server
        │
        ▼
 TCP reassembles bytes
        │
        ▼
 Web Server sees
   HTTP Request
        │
        ▼
  Processes Request
        │
        ▼
  Creates HTTP Response
        │
        ▼
      TCP
        │
        ▼
       IP
        │
        ▼
     Network
        │
        ▼
      Browser
        │
        ▼
   Renders Web Page
```

**Key Points**
- DNS translates the hostname into an IP address.
- TCP establishes reliable transport before HTTP data is sent.
- The browser creates the HTTP request.
- HTTP defines the meaning of the request; TCP transports its bytes.
- TCP segments the HTTP bytes and IP carries packets across the network.
- The server reverses the process and interprets the reconstructed HTTP request.
- The server sends an HTTP response back to the browser.
- The browser may make many additional HTTP requests for page resources.