# TCP Three-Way Handshake

```text
Client                          Server

   SYN (Seq=1000)
------------------------------->

             SYN + ACK
      (Seq=5000, Ack=1001)
<-------------------------------

 ACK (Ack=5001)
------------------------------->

      Connection Established
```

**Key Points**
- SYN initiates a TCP connection.
- SYN-ACK acknowledges the client and sends the server's initial sequence number.
- ACK completes the handshake.
- Data transfer begins only after the handshake completes.