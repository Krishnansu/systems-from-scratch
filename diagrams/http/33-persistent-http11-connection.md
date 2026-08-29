# HTTP/1.1 Persistent Connection

```text
                  One TCP Connection
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
   HTTP Request 1   HTTP Request 2   HTTP Request 3
        |                |                |
        v                v                v
   HTTP Response 1  HTTP Response 2  HTTP Response 3
        |                |                |
        +----------------+----------------+
                         |
                         v
                  Connection Close
```

**Without Persistence**

```text
TCP Connection 1
    |
    +-- Request 1
    +-- Response 1
    +-- CLOSE

TCP Connection 2
    |
    +-- Request 2
    +-- Response 2
    +-- CLOSE
```

**With Persistence**

```text
TCP Connection
    |
    +-- Request 1 -> Response 1
    |
    +-- Request 2 -> Response 2
    |
    +-- Request 3 -> Response 3
    |
    +-- CLOSE
```

**Key Points**
- HTTP remains stateless even when the TCP connection persists.
- Persistent connections allow multiple HTTP exchanges over one TCP connection.
- Reusing the connection avoids establishing a new TCP connection for every request.
- Persistent does not mean permanent.