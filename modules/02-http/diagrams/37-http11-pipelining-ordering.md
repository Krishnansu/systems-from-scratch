# HTTP/1.1 Request Ordering and Pipelining

```text
Client                                      Server

GET /a
------------------------------------------->

GET /b
------------------------------------------->

GET /c
------------------------------------------->

                  Process /a
                  Process /b
                  Process /c

<-------------------------------------------
HTTP 200 OK /a

<-------------------------------------------
HTTP 200 OK /b

<-------------------------------------------
HTTP 200 OK /c
```

### Head-of-Line Blocking Example

```text
Request A: Slow
Request B: Fast
Request C: Fast

A ---------------------> Server
B ---------------------> Server
C ---------------------> Server

A processing: 10 seconds

             WAIT
              |
              v
Response A --------------------->
Response B --------------------->
Response C --------------------->
```

**Key Points**
- HTTP/1.1 pipelining allows multiple requests to be sent without waiting for every response.
- Responses must preserve request ordering.
- A slow earlier request can delay later responses.
- This limitation is one motivation for HTTP/2 multiplexing.